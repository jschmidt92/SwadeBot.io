from dotenv import load_dotenv
import customtkinter as ctk
import json
import os
import requests
import tkinter as tk

load_dotenv()

MAIN_WEBHOOK_URL = os.getenv("MAIN_WEBHOOK_URL")


class CTkEntryWithPlaceholder(ctk.CTkEntry):
    def __init__(self, master=None, placeholder_text="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder_text = placeholder_text
        self.insert("end", self.placeholder_text)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, event):
        if self.get() == self.placeholder_text:
            self.delete(0, "end")

    def on_focus_out(self, event):
        if not self.get():
            self.insert("end", self.placeholder_text)


class CharacterFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self, text="Character Module")
        self.label.grid(row=0, column=0, columnspan=2)

        self.character_id_var = ctk.StringVar()
        self.character_name_var = ctk.StringVar()
        self.pace_var = ctk.StringVar()
        self.parry_var = ctk.StringVar()
        self.toughness_var = ctk.StringVar()
        self.attributes_var = ctk.StringVar()
        self.skills_var = ctk.StringVar()
        self.gear_var = ctk.StringVar()
        self.hindrances_var = ctk.StringVar()
        self.edges_var = ctk.StringVar()
        self.money_var = ctk.StringVar()

        self.character_id_entry = CTkEntryWithPlaceholder(
            self,
            textvariable=self.character_id_var,
            placeholder_text="Enter Character ID",
        )
        self.character_id_entry.grid(row=1, column=0, padx=5, pady=5)

        self.character_name_entry = CTkEntryWithPlaceholder(
            self,
            textvariable=self.character_name_var,
            placeholder_text="Enter Character Name",
        )
        self.character_name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.pace_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.pace_var, placeholder_text="Enter Pace Value"
        )
        self.pace_entry.grid(row=3, column=0, padx=5, pady=5)

        self.parry_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.parry_var, placeholder_text="Enter Parry Value"
        )
        self.parry_entry.grid(row=3, column=1, padx=5, pady=5)

        self.toughness_entry = CTkEntryWithPlaceholder(
            self,
            textvariable=self.toughness_var,
            placeholder_text="Enter Toughness Value",
        )
        self.toughness_entry.grid(row=4, column=0, padx=5, pady=5)

        self.attributes_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.attributes_var, placeholder_text="Enter Attributes"
        )
        self.attributes_entry.grid(row=5, column=0, padx=5, pady=5)

        self.skills_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.skills_var, placeholder_text="Enter Skills"
        )
        self.skills_entry.grid(row=5, column=1, padx=5, pady=5)

        self.gear_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.gear_var, placeholder_text="Enter Gear"
        )
        self.gear_entry.grid(row=6, column=0, padx=5, pady=5)

        self.hindrances_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.hindrances_var, placeholder_text="Enter Hindrances"
        )
        self.hindrances_entry.grid(row=6, column=1, padx=5, pady=5)

        self.edges_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.edges_var, placeholder_text="Enter Edges"
        )
        self.edges_entry.grid(row=7, column=0, padx=5, pady=5)

        self.money_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.money_var, placeholder_text="Enter Money Value"
        )
        self.money_entry.grid(row=4, column=1, padx=5, pady=5)

        self.character_id_entry.bind("<FocusIn>", self.clear_placeholder)
        self.character_name_entry.bind("<FocusIn>", self.clear_placeholder)
        self.pace_entry.bind("<FocusIn>", self.clear_placeholder)
        self.parry_entry.bind("<FocusIn>", self.clear_placeholder)
        self.toughness_entry.bind("<FocusIn>", self.clear_placeholder)
        self.attributes_entry.bind("<FocusIn>", self.clear_placeholder)
        self.skills_entry.bind("<FocusIn>", self.clear_placeholder)
        self.gear_entry.bind("<FocusIn>", self.clear_placeholder)
        self.hindrances_entry.bind("<FocusIn>", self.clear_placeholder)
        self.edges_entry.bind("<FocusIn>", self.clear_placeholder)
        self.money_entry.bind("<FocusIn>", self.clear_placeholder)

        self.send_create_character_button = ctk.CTkButton(
            self, text="Create Character", command=self.create_character
        )
        self.send_create_character_button.grid(row=9, column=0, padx=5, pady=5)

        self.send_create_monster_button = ctk.CTkButton(
            self, text="Create Monster", command=self.create_monster
        )
        self.send_create_monster_button.grid(row=10, column=0, padx=5, pady=5)

        self.send_update_character_button = ctk.CTkButton(
            self, text="Update Character", command=self.update_character
        )
        self.send_update_character_button.grid(row=9, column=1, padx=5, pady=5)

        self.send_update_monster_button = ctk.CTkButton(
            self, text="Update Monster", command=self.update_monster
        )
        self.send_update_monster_button.grid(row=10, column=1, padx=5, pady=5)

    def clear_placeholder(self, event):
        event.widget.delete(0, "end")

    def send_command(self, message):
        webhook_url = MAIN_WEBHOOK_URL
        headers = {"Content-Type": "application/json"}
        data = {"content": message, "username": "GameMaster"}

        def send_request():
            response = requests.post(
                webhook_url, headers=headers, data=json.dumps(data)
            )
            if response.status_code == 204:
                print(f"Successfully sent message: {message}")
            else:
                print(f"Failed to send message. Status code: {response.status_code}")

        self.executor.submit(send_request)

    def create_character(self):
        player_id = self.player_id_var.get()
        character_name = self.character_name_var.get()
        pace = self.pace_var.get()
        parry = self.parry_var.get()
        toughness = self.toughness_var.get()
        attributes = self.attributes_var.get()
        skills = self.skills_var.get()
        gear = self.gear_var.get()
        hindrances = self.hindrances_var.get()
        edges = self.edges_var.get()
        money = self.money_var.get()
        self.send_create_character(
            player_id,
            character_name,
            pace,
            parry,
            toughness,
            attributes,
            skills,
            gear,
            hindrances,
            edges,
            money,
        )

    def create_monster(self):
        monster_id = self.character_id_var.get()
        monster_name = self.character_name_var.get()
        pace = self.pace_var.get()
        parry = self.parry_var.get()
        toughness = self.toughness_var.get()
        attributes = self.attributes_var.get()
        skills = self.skills_var.get()
        gear = self.gear_var.get()
        hindrances = self.hindrances_var.get()
        edges = self.edges_var.get()
        money = self.money_var.get()
        self.send_create_character(
            monster_id,
            monster_name,
            pace,
            parry,
            toughness,
            attributes,
            skills,
            gear,
            hindrances,
            edges,
            money,
        )

    def update_character(self):
        self.send_update_character()

    def update_monster(self):
        self.send_update_monster()

    def send_create_character(
        self,
        character_id,
        character_name,
        pace,
        parry,
        toughness,
        attributes,
        skills,
        gear,
        hindrances,
        edges,
        money,
    ):
        command = "!create_character"
        message = f"{command} {character_id} {character_name} {pace} {parry} {toughness} {attributes} {skills} {gear} {hindrances} {edges} {money}"
        self.send_command(message)

    def send_create_character(
        self,
        monster_name,
        pace,
        parry,
        toughness,
        attributes,
        skills,
        gear,
        hindrances,
        edges,
        money,
    ):
        command = "!create_monster"
        message = f"{command} {monster_name} {pace} {parry} {toughness} {attributes} {skills} {gear} {hindrances} {edges} {money}"
        self.send_command(message)

    def send_update_character(
        self,
        character_id,
        character_name,
        pace,
        parry,
        toughness,
        attributes,
        skills,
        gear,
        hindrances,
        edges,
        money,
    ):
        command = "!update_character"
        message = f"{command} {character_id} {character_name} {pace} {parry} {toughness} {attributes} {skills} {gear} {hindrances} {edges} {money}"
        self.send_command(message)

    def send_update_monster(
        self,
        monster_id,
        monster_name,
        pace,
        parry,
        toughness,
        attributes,
        skills,
        gear,
        hindrances,
        edges,
        money,
    ):
        command = "!update_monster"
        message = f"{command} {monster_id} {monster_name} {pace} {parry} {toughness} {attributes} {skills} {gear} {hindrances} {edges} {money}"
        self.send_command(message)
