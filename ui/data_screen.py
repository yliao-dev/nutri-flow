import customtkinter as ctk

class DataScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Example content for the data screen
        label = ctk.CTkLabel(self, text="Data Screen", font=("Arial", 18))
        label.pack(pady=20)