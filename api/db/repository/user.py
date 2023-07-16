from sqlalchemy.orm import Session

from db.models.user import User
from schemas.user import UserCreate, UpdateUser


def create_new_user(user: UserCreate, db: Session):
    user_orm = User(
        username=user.username,
        discord_id=user.discord_id,
    )
    db.add(user_orm)
    db.commit()
    db.refresh(user_orm)
    return user_orm


def retrieve_user(discord_id: int, db: Session):
    row = db.query(User).filter(User.discord_id == discord_id).first()
    if row is None:
        return None
    return row


def list_users(db: Session):
    rows = db.query(User).all()
    if rows is None:
        return None
    return rows


def update_user(user_id: int, user: UpdateUser, db: Session):
    user_data = db.query(User).filter(User.id == user_id).first()
    if user_data is None:
        return None
    for var, value in user.dict(exclude_unset=True).items():
        setattr(user_data, var, value)
    db.commit()
    db.refresh(user_data)
    return user_data


def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    db.delete(user)
    db.commit()
    return user
