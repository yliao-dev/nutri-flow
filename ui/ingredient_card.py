import customtkinter as ctk

class IngredientCard(ctk.CTkFrame):
    """
    Represents a single ingredient card in the nutrition progress screen.
    """
    def __init__(self, parent, index, width=500, height=550):
        super().__init__(parent, fg_color="#e0e0e0", corner_radius=10, width=width, height=height)

        # Ingredient card content
        self.index = index
        self.card_label = ctk.CTkLabel(self, text=f"Ingredient {self.index + 1}", font=("Arial", 12))
        self.card_label.pack(pady=(10, 0), expand=True)

        # Checkbox
        self.checkbox = ctk.CTkCheckBox(self, text="")
        self.checkbox.pack(side="bottom", anchor="se", padx=5, pady=(0, 10))