import customtkinter as ctk

from tkinter import messagebox

from frames.economy import EconomyFrame
from frames.initiative import InitiativeFrame
from frames.character import CharacterFrame

from models.EncounterModel import Encounter
from models.MoneyModel import Money

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


class SwadeBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x768")
        self.resizable(True, True)

        self.money = Money()
        self.title("SwadeBot App")

        self.initiative_frame = InitiativeFrame(master=self)
        self.initiative_frame.grid(
            row=1, column=0, columnspan=1, padx=(20, 10), pady=10, sticky="nsew"
        )

        self.economy_frame = EconomyFrame(master=self)
        self.economy_frame.grid(
            row=1, column=1, columnspan=1, padx=10, pady=10, sticky="nsew"
        )

        self.character_frame = CharacterFrame(master=self)
        self.character_frame.grid(
            row=0, column=0, columnspan=2, padx=(20, 30), pady=10, sticky="nsew"
        )

    def clear_inputs(self):
        self.economy_frame.player_id_var.set("")
        self.economy_frame.character_name_var.set("")
        self.economy_frame.amount_var.set("")

    def give_money(self):
        player_id = int(self.economy_frame.player_id_var.get())
        character_name = str(self.economy_frame.character_name_var.get())
        amount = int(self.economy_frame.amount_var.get())

        self.money.add(player_id, character_name, amount)

        messagebox.showinfo(
            "Success", f"Gave {amount} money to {character_name} of {player_id}"
        )

        self.clear_inputs()

    def take_money(self):
        player_id = int(self.economy_frame.player_id_var.get())
        character_name = str(self.economy_frame.character_name_var.get())
        amount = int(self.economy_frame.amount_var.get())

        current_money = self.money.read(player_id, character_name)
        if current_money[0] < amount:
            messagebox.showerror(
                "Error", f"{character_name} of {player_id} doesn't have enough money"
            )
            return

        self.money.subtract(player_id, character_name, amount)

        messagebox.showinfo(
            "Success", f"Took {amount} money from {character_name} of {player_id}"
        )

        self.clear_inputs()

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = SwadeBotApp()
    app.run()
