import customtkinter as ctk


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


class EconomyFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self, text="Economy Module")
        self.label.grid(row=0, column=0, columnspan=2)

        self.player_id_var = ctk.StringVar()
        self.character_name_var = ctk.StringVar()
        self.amount_var = ctk.StringVar()

        self.player_id_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.player_id_var, placeholder_text="Enter Player ID"
        )
        self.player_id_entry.grid(row=1, column=0, padx=5, pady=5)

        self.character_name_entry = CTkEntryWithPlaceholder(
            self,
            textvariable=self.character_name_var,
            placeholder_text="Enter Character Name",
        )
        self.character_name_entry.grid(row=2, column=0, padx=5, pady=5)

        self.amount_entry = CTkEntryWithPlaceholder(
            self, textvariable=self.amount_var, placeholder_text="Enter Amount"
        )
        self.amount_entry.grid(row=3, column=0, padx=5, pady=5)

        self.player_id_entry.bind("<FocusIn>", self.clear_placeholder)
        self.character_name_entry.bind("<FocusIn>", self.clear_placeholder)
        self.amount_entry.bind("<FocusIn>", self.clear_placeholder)

        self.give_money_button = ctk.CTkButton(
            self, text="Give Money", command=master.give_money
        )
        self.give_money_button.grid(row=4, column=0, padx=5, pady=5)

        self.take_money_button = ctk.CTkButton(
            self, text="Take Money", command=master.take_money
        )
        self.take_money_button.grid(row=5, column=0, padx=5, pady=5)

    def clear_placeholder(self, event):
        event.widget.delete(0, "end")
