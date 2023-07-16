from dotenv import load_dotenv
import concurrent.futures
import customtkinter as ctk
import json
import os
import requests

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


class InitiativeFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self, text="Initiative Module")
        self.label.grid(row=0, column=0, columnspan=2)

        self.encounter_id_var = ctk.StringVar()
        self.player_name_var = ctk.StringVar()

        self.encounter_id_entry = CTkEntryWithPlaceholder(
            self,
            textvariable=self.encounter_id_var,
            placeholder_text="Enter Encounter ID",
        )
        self.encounter_id_entry.grid(row=1, column=0, padx=5, pady=5)

        self.player_name_entry = CTkEntryWithPlaceholder(
            self,
            textvariable=self.player_name_var,
            placeholder_text="Enter Player Name",
        )
        self.player_name_entry.grid(row=2, column=0, padx=5, pady=5)

        self.encounter_id_entry.bind("<FocusIn>", self.clear_placeholder)
        self.player_name_entry.bind("<FocusIn>", self.clear_placeholder)

        self.send_encounter_id_button = ctk.CTkButton(
            self,
            text="Deal Initiative",
            command=self.deal_initiative,
        )
        self.send_encounter_id_button.grid(row=3, column=0, padx=5, pady=5)

        self.send_next_turn_button = ctk.CTkButton(
            self,
            text="Next Turn",
            command=self.next_turn,
        )
        self.send_next_turn_button.grid(row=4, column=0, padx=5, pady=5)

        self.send_end_initiative_button = ctk.CTkButton(
            self,
            text="End Initiative",
            command=self.end_initiative,
        )
        self.send_end_initiative_button.grid(row=5, column=0, padx=5, pady=5)

        self.send_player_name_button = ctk.CTkButton(
            self,
            text="Deal Card",
            command=self.deal_card,
        )
        self.send_player_name_button.grid(row=6, column=0, padx=5, pady=5)

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

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

    def deal_initiative(self):
        encounter_id = self.encounter_id_var.get()
        self.send_deal_initiative(
            encounter_id,
        )

    def next_turn(self):
        self.send_next_turn()

    def end_initiative(self):
        self.send_end_initiative()

    def deal_card(self):
        player_name = self.player_name_var.get()
        self.send_deal_card(
            player_name,
        )

    def view_player_cards(self):
        player_name = self.player_name_var.get()
        self.send_view_player_cards(
            player_name,
        )

    def send_deal_initiative(self, encounter_id):
        command = "!deal_initiative"
        message = f"{command} {encounter_id}"
        self.send_command(message)

    def send_next_turn(self):
        command = "!next_turn"
        message = f"{command}"
        self.send_command(message)

    def send_end_initiative(self):
        command = "!end_initiative"
        message = f"{command}"
        self.send_command(message)

    def send_deal_card(self, player_name):
        command = "!deal_card"
        message = f"{command} {player_name}"
        self.send_command(message)
