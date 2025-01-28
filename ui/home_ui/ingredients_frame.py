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
        cards_per_row = self.calculate_cards_per_row()

        # Clear the current ingredient cards before repopulating
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.ingredient_cards.clear()

        def display_card_with_animation(index):
            if index >= len(self.ingredients_data):
                return  # Stop if all cards are displayed

            ingredient = self.ingredients_data[index]
            row = index // cards_per_row
            col = index % cards_per_row

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
            self.ingredient_cards.append(ingredient_card)

            # Start fade-in animation
            self.fade_in_card(ingredient_card)

            # Schedule the next card
            self.after(50, lambda: display_card_with_animation(index + 1))

        # Start displaying the cards
        display_card_with_animation(0)

        # Configure column weights to ensure equal width
        for col in range(cards_per_row):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)


    def fade_in_card(self, card):
        """Simulate a fade-in effect with visibility checks."""
        opacity_levels = [0.1 * i for i in range(1, 11)]  # Gradual increase in visibility

        def set_opacity(level_index):
            if level_index >= len(opacity_levels):
                return  # Stop the animation once fully visible

            # Check if the widget still exists
            if not str(card).startswith("."):
                return  # Stop if the widget was destroyed

            card.update_idletasks()  # Force UI redraw
            card.master.update_idletasks()

            # Ensure the card is visible (grid)
            try:
                card.grid()
            except Exception:
                return  # Prevent errors if the widget no longer exists

            self.after(30, lambda: set_opacity(level_index + 1))  # Adjust speed of fade-in

        set_opacity(0)