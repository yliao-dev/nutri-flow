import customtkinter as ctk

class IngredientScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Example content for the ingredient screen
        label = ctk.CTkLabel(self, text="Ingredient Screen", font=("Arial", 18))
        label.pack(pady=20)