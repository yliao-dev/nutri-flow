import customtkinter as ctk
from PIL import Image


class IngredientCard(ctk.CTkFrame):
    """Graphical representation of an ingredient with selection and serving size input."""

    # Tracks the currently selected card for detail view (only one at a time)
    currently_selected_card = None

    def __init__(self, parent, index, ingredient_data, update_selected_data_callback, selection_type, width, height):
        super().__init__(parent, corner_radius=0, width=width, height=height)
        self.grid_propagate(False)

        self.ingredient_data = ingredient_data
        self.index = index
        self.update_selected_data_callback = update_selected_data_callback
        self.selection_type = selection_type  # 'intake' (multiple selection) or 'detail' (single selection)
        self.selected = False

        # Card layout configuration
        for row in range(5):
            self.grid_rowconfigure(row, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Colors for selection highlighting
        self.highlight_color = "#2980B9"
        self.default_border_color = self.cget("fg_color")

        # UI elements
        self.card_label = None
        self.protein_label = None
        self.carbs_label = None
        self.fat_label = None
        self.image_label = None

    def add_name(self):
        """Adds the ingredient name label and binds click events for selection."""
        if not self.card_label:
            self.card_label = ctk.CTkLabel(
                self, text=self.ingredient_data['name'].replace('_', ' ').title(), font=("Arial", 14, "bold")
            )
            self.card_label.grid(row=0, column=0, pady=(10, 0))
            self.bind_interaction(self.card_label)

    def add_nutrition_data(self):
        """Displays protein, carbohydrate, and fat content."""
        if not self.protein_label:
            self.protein_label = ctk.CTkLabel(self, text=f"Protein: {self.ingredient_data['nutrition']['protein']}g")
            self.protein_label.grid(row=1, column=0, pady=(0, 5))
            self.bind_interaction(self.protein_label)

        if not self.carbs_label:
            self.carbs_label = ctk.CTkLabel(self, text=f"Carbohydrate: {self.ingredient_data['nutrition']['carbohydrate']}g")
            self.carbs_label.grid(row=2, column=0, pady=(0, 5))
            self.bind_interaction(self.carbs_label)

        if not self.fat_label:
            self.fat_label = ctk.CTkLabel(self, text=f"Fat: {self.ingredient_data['nutrition']['fat']}g")
            self.fat_label.grid(row=3, column=0, pady=(0, 10))
            self.bind_interaction(self.fat_label)

    def add_image(self, image_path=None):
        """Adds an image to the card if a valid path is provided."""
        if image_path and not self.image_label:
            img = Image.open(image_path).convert("RGBA").resize((100, 100))
            img_ctk = ctk.CTkImage(img, size=(100, 100))

            self.image_label = ctk.CTkLabel(self, image=img_ctk, text=None)
            self.image_label.image = img_ctk
            self.image_label.grid(row=4, column=0, pady=(10, 5))
            self.bind_interaction(self.image_label)

    def bind_interaction(self, widget):
        """Binds hover and click events to a given widget."""
        widget.bind("<Enter>", self.on_hover)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<Button-1>", self.toggle_select)

    def toggle_select(self, event=None):
        """Handles selection behavior based on selection type ('intake' or 'detail')."""
        if self.selection_type == 'intake':
            self.toggle_select_intake()
        elif self.selection_type == 'detail':
            self.toggle_select_detail()

    def toggle_select_intake(self):
        """Toggles selection for intake tracking (allows multiple selections)."""
        self.selected = not self.selected
        self.configure(fg_color=self.highlight_color if self.selected else self.default_border_color)

        if self.selected:
            self.on_serving_size_change()
            self.update_selected_data_callback(self.ingredient_data, add=True)
        else:
            self.update_selected_data_callback(self.ingredient_data, add=False)

    def toggle_select_detail(self):
        """Ensures only one ingredient card is selected at a time for detail view."""
        if IngredientCard.currently_selected_card and IngredientCard.currently_selected_card != self:
            IngredientCard.currently_selected_card.deselect()

        self.selected = True
        self.configure(fg_color=self.highlight_color)
        IngredientCard.currently_selected_card = self
        self.update_selected_data_callback(self.ingredient_data)

    def deselect(self):
        """Deselects the card and resets its border color."""
        self.selected = False
        self.configure(fg_color=self.default_border_color)

    def on_hover(self, event=None):
        """Highlights the card when hovered if it's not selected."""
        if not self.selected:
            self.configure(fg_color="lightgrey")

    def on_leave(self, event=None):
        """Restores the original color when the hover ends."""
        if not self.selected:
            self.configure(fg_color=self.default_border_color)

    def add_custom_serving_size(self):
        """Adds an entry field for custom serving size input."""
        if not hasattr(self, 'serving_size_entry'):
            self.serving_size_var = ctk.StringVar(value=self.ingredient_data.get("custom_serving_size", 100))

            self.serving_size_entry = ctk.CTkEntry(
                self, width=200, font=("Arial", 14), placeholder_text="Enter serving size in grams",
                textvariable=self.serving_size_var, validate="key",
                validatecommand=(self.register(self.validate_serving_size_input), "%P")
            )
            self.serving_size_entry.grid(row=5, column=0, pady=(10, 0))

    def on_serving_size_change(self, event=None):
        """Updates the ingredient data with the new serving size if valid."""
        try:
            self.ingredient_data["custom_serving_size"] = float(self.serving_size_var.get())
        except ValueError:
            print("Invalid serving size entered.")

    def validate_serving_size_input(self, value):
        """Validates that the serving size input contains only numbers and at most one decimal point."""
        return value == "" or value.isdigit() or (value.count('.') == 1 and value.replace('.', '').isdigit())