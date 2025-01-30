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
        # Calculate number of columns once
        self.cards_per_row = self.calculate_cards_per_row()

        # Clear the current ingredient cards before repopulating
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.ingredient_cards.clear()

        # Ensure column weights are correctly set
        for col in range(self.cards_per_row):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)

        # Start displaying cards one by one
        self.display_card_with_animation(0)

    def display_card_with_animation(self, index):
        """Recursively display ingredient cards with one-by-one animation, ensuring each row fills before new ones appear."""
        
        if index >= len(self.ingredients_data):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # Ensure scrolling updates correctly
            return  # Stop if all cards are placed

        ingredient = self.ingredients_data[index]
        row = index // self.cards_per_row
        col = index % self.cards_per_row

        # Create ingredient card
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

        # Place card in correct row and column
        ingredient_card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        self.ingredient_cards.append(ingredient_card)

        # Ensure the row is correctly sized
        self.scrollable_frame.grid_rowconfigure(row, weight=1)

        # Start fade-in animation and schedule the next card a bit earlier
        self.fade_in_card(ingredient_card, lambda: self.after(10, lambda: self.display_card_with_animation(index + 1)))

    def fade_in_card(self, card, callback):
        """Simulate a fade-in effect with controlled timing to prevent skipping."""
        opacity_levels = [0.2 * i for i in range(1, 6)]  # Gradual visibility increase

        def set_opacity(level_index):
            if level_index >= len(opacity_levels):
                callback()  # Only trigger the next card when fade-in is complete
                return

            if not str(card).startswith("."):
                return  # Stop if widget is destroyed

            card.update_idletasks()  # Force UI redraw
            card.master.update_idletasks()

            # Ensure the card remains visible in the grid
            try:
                card.grid()
            except Exception:
                return  # Prevent errors if the widget is gone

            self.after(10, lambda: set_opacity(level_index + 1))

        set_opacity(0)