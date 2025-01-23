import customtkinter as ctk
from ui.home_ui.progress_frame import ProgressFrame
from ui.ingredients_ui.ingredient_card import IngredientCard
from ui.home_ui.bottom_frame import BottomFrame
from PIL import Image
from config import DARK_MODE_IMG
from model.data_manager import load_from_ingredients_json, sort_ingredients

class HomeScreen(ctk.CTkFrame):
    def __init__(self, master, nutrition_view_model):
        super().__init__(master)
        self.resize_debounce = None
        
        self.nutrition_view_model = nutrition_view_model
        self.ingredients_data = load_from_ingredients_json()
        sorted_ingredients = sort_ingredients(self.ingredients_data, criteria="frequency_of_use")
        self.ingredients_data = sorted_ingredients
        self.user_goals = {
            "protein": self.nutrition_view_model.user_nutrition_model.goal_protein,
            "carbohydrate": self.nutrition_view_model.user_nutrition_model.goal_carbohydrate,
            "fat": self.nutrition_view_model.user_nutrition_model.goal_fat,
            "calories": self.nutrition_view_model.user_nutrition_model.goal_calories,
        }

        self.progress_frames = {}  # Dictionary to store the progress frames
        self.ingredient_cards = []  # List to store IngredientCard instances
        self.initialize_ui()

    def initialize_ui(self):
        self.label = ctk.CTkLabel(self, text="Nutrition Progress", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=1, columnspan=1, pady=5, sticky="nsew") 
        self.weight_label = ctk.CTkLabel(
                    self,
                    font=("Arial", 16, "bold"),
                    text=f"Weight: {self.nutrition_view_model.user_nutrition_model.weight}kg",
                    fg_color="transparent", 
                )
        self.weight_label.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.date_label = ctk.CTkLabel(
                    self,
                    font=("Arial", 16, "bold"),
                    text=f"Date: {self.nutrition_view_model.user_nutrition_model.date}",
                    fg_color="transparent", 
                )
        # self.date_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.sorting_var = ctk.StringVar(value="Sort by")
        self.sorting_menu = ctk.CTkOptionMenu(self, variable=self.sorting_var, values=["Frequency", "Alphabetical", "Recently Used"],
                                        command=self.apply_sorting)
        self.sorting_menu.grid(row=0, column=0, padx=10, pady=10)
        
        # Appearance Mode Selector (using a single image)
        self.mode_img = ctk.CTkImage(light_image=Image.open(DARK_MODE_IMG), size=(40, 40))
        self.mode_label = ctk.CTkLabel(
            self,
            text="", 
            image=self.mode_img, 
            fg_color="transparent", 
        )
        self.mode_label.bind("<Button-1>", lambda event: self.toggle_appearance_mode())
        # Prevent any hover effect
        self.mode_label.bind("<Enter>", lambda event: self.mode_label.configure(fg_color="transparent"))
        self.mode_label.bind("<Leave>", lambda event: self.mode_label.configure(fg_color="transparent"))
        self.mode_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")
    
        # Configure the grid
        self.configure_grid()
       
        self.create_progress_frames()
        self.create_ingredients_frame()
        self.populate_ingredient_cards()
        self.create_bottom_frame()

    def configure_grid(self):
        for column in range(3):
            self.grid_columnconfigure(column, weight=1, uniform="nutrition")
        self.grid_rowconfigure(1, weight=2, minsize=150)  # Adjusted minsize for better display
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=1)

    def create_progress_frames(self):
        goal_names = ["protein", "carbohydrate", "fat"]
        consumed_values = self.nutrition_view_model.get_nutrition_data()
        goal_values = self.user_goals

        for index, goal_name in enumerate(goal_names):
            self.progress_frames[goal_name] = self.create_single_progress_frame(goal_name, index, consumed_values, goal_values)

    def create_single_progress_frame(self, goal_name, column_index, consumed_values, goal_values):
        progress_frame = ProgressFrame(
            master=self,
            goal_name=goal_name,
            goal_values=goal_values,
            consumed_value=consumed_values,
            update_callback=ProgressFrame.update_nutrition_label,
        )
        progress_frame.grid(row=1, column=column_index, padx=10, pady=10, sticky="nsew")
        return progress_frame

    def create_ingredients_frame(self):
        self.ingredients_frame = ctk.CTkFrame(self)
        self.ingredients_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=0, sticky="nsew")

        self.ingredients_frame.bind("<Configure>", self.on_frame_resize)  # Bind resize event
        
        self.canvas = ctk.CTkCanvas(self.ingredients_frame, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.ingredients_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def on_frame_resize(self, event):
        # Recalculate the number of cards per row when the frame size changes
        if self.resize_debounce is not None:
            self.after_cancel(self.resize_debounce)
        
        # Schedule the function to be called after 200 ms (adjust this as needed)
        self.resize_debounce = self.after(0, self.populate_ingredient_cards)


    def calculate_cards_per_row(self):
        frame_width = self.ingredients_frame.winfo_width()        
        card_width = 150
        cards_per_row = frame_width // card_width
        return max(3, cards_per_row)
    
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
                update_selected_data_callback=self.update_bottom_frame,
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

    def update_bottom_frame(self, ingredients_data, add):
        self.bottom_frame.update_selected_data(ingredients_data, add)

    def create_bottom_frame(self):
        self.bottom_frame = BottomFrame(
            master=self,
            nutrition_view_model=self.nutrition_view_model,
            update_intake_callback=self.update_intake,
            ingredient_cards=self.ingredient_cards,
        )
        self.bottom_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def update_intake(self, nutrition_data):
        # Update each progress frame with the new data
        for _, progress_frame in self.progress_frames.items():
            progress_frame.update(nutrition_data)
            
            
    def toggle_appearance_mode(self):
        """Toggle between light and dark mode when clicked."""
        current_mode = ctk.get_appearance_mode()

        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")  # Switch to light mode
        else:
            ctk.set_appearance_mode("Dark")  # Switch to dark mode
            
    def apply_sorting(self, selected_option):
        # Map selected options to the corresponding sorting criteria
        if selected_option == "Frequency":
            criteria = "frequency_of_use"
            descending = True
            print("Sorting by frequency.")
        elif selected_option == "Alphabetical":
            criteria = "name"  # Assuming 'id' or another key is used for alphabetical sorting
            print("Sorting alphabetically.")
            descending = False
        elif selected_option == "Recently Used":
            criteria = "last_used_date"
            descending = True
            print("Sorting by recent usage.")

        # Sort the ingredients data based on the selected criteria
        self.ingredients_data = sort_ingredients(self.ingredients_data, criteria, descending)
        ingredient_keys = [ingredient["name"] for ingredient in self.ingredients_data if "name" in ingredient]
        print(ingredient_keys)
        # self.populate_ingredient_cards()