import customtkinter as ctk
from ui.ingredients_ui.ingredient_card import IngredientCard

class IngredientsFrame(ctk.CTkFrame):
    def __init__(self, master, ingredients_data, update_bottom_frame_callback):
        super().__init__(master)
        self.ingredients_data = ingredients_data
        self.update_bottom_frame_callback = update_bottom_frame_callback
        self.resize_debounce = None
        self.ingredient_cards = []  # List to store IngredientCard instances

        self.create_scrollable_frame()
        self.populate_ingredient_cards()

    def create_scrollable_frame(self):
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.bind("<Configure>", self.on_frame_resize)

    def on_frame_resize(self, event):
        # Recalculate the number of cards per row when the frame size changes
        if self.resize_debounce is not None:
            self.after_cancel(self.resize_debounce)
        
        self.resize_debounce = self.after(10, self.populate_ingredient_cards)

    def calculate_cards_per_row(self):
        frame_width = self.winfo_width()
        card_width = 150
        return max(3, frame_width // card_width)

    
    def populate_ingredient_cards(self):
        # Get the number of cards per row based on the current frame size
        cards_per_row = self.calculate_cards_per_row()

        # Clear the current ingredient cards before repopulating
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.ingredient_cards.clear()  # Reset the list of ingredient cards

        for i, ingredient in enumerate(self.ingredients_data):
            # Calculate row and column position
            row = i // cards_per_row
            col = i % cards_per_row

            ingredient_card = IngredientCard(
                self.scrollable_frame,
                index=ingredient["id"],
                ingredient_data=ingredient,
                update_selected_data_callback=self.update_bottom_frame_callback,
                selection_type="intake",
                width=150,
                height=250
            )
            ingredient_card.add_name()
            ingredient_card.add_nutrition_data()
            ingredient_card.add_image(ingredient["image"])
            ingredient_card.add_custom_serving_size()

            # Place the card in the grid
            ingredient_card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            # Add the card to the list
            self.ingredient_cards.append(ingredient_card)

        # Configure column weights to ensure equal width
        for col in range(cards_per_row):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)