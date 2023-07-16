from flask import Flask, g, redirect, request, send_from_directory, session
from zenora import APIClient
from core.config import settings
from db.session import get_db
import sqlite3

flask_app = Flask(__name__, static_folder="./static")
flask_app.config["SECRET_KEY"] = "verysecret"
client = APIClient(settings.TOKEN, client_secret=settings.CLIENT_SECRET)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("swade.db")
    return db


@flask_app.route("/api/oauth/callback")
def callback():
    code = request.args["code"]
    access_token = client.oauth.get_access_token(
        code, settings.REDIRECT_URI
    ).access_token

    session["token"] = access_token

    bearer_client = APIClient(access_token, bearer=True)
    discord_user = bearer_client.users.get_current_user()

    current_user = {"id": discord_user.id, "username": discord_user.username}

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE discord_id = ?", (current_user["id"],))
    user = cursor.fetchone()

    if user:
        return redirect(
            f"http://135.135.196.140?token={access_token}&discord_id={current_user['id']}"
        )
    else:
        cursor.execute(
            "INSERT INTO users (discord_id, username) VALUES (?, ?)",
            (current_user["id"], current_user["username"]),
        )
        db.commit()

    return redirect("/")


@flask_app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        flask_app.static_folder, "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@flask_app.route("/style.css")
def style():
    return send_from_directory(flask_app.static_folder, "./css/style.css")
