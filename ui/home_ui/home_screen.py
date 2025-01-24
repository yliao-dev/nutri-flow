import customtkinter as ctk
from ui.home_ui.progress_frame import ProgressFrame
from ui.home_ui.ingredients_frame import IngredientsFrame  # Import IngredientsFrame
from ui.home_ui.bottom_frame import BottomFrame
from PIL import Image
from config import DARK_MODE_IMG
from model.data_manager import load_from_ingredients_json, sort_ingredients
from ui.splash_screen import SplashScreen  # Assuming SplashScreen is a separate widget

class HomeScreen(ctk.CTkFrame):
    def __init__(self, master, nutrition_view_model):
        super().__init__(master)
        self.resize_debounce = None
        
        self.nutrition_view_model = nutrition_view_model
        self.ingredients_data = []
        self.sorted_ingredients = []
        self.user_goals = {
            "protein": self.nutrition_view_model.user_nutrition_model.goal_protein,
            "carbohydrate": self.nutrition_view_model.user_nutrition_model.goal_carbohydrate,
            "fat": self.nutrition_view_model.user_nutrition_model.goal_fat,
            "calories": self.nutrition_view_model.user_nutrition_model.goal_calories,
        }

        self.progress_frames = {}  # Dictionary to store the progress frames
        self.ingredient_cards = []  # List to store IngredientCard instances
        self.splash_screen = SplashScreen(master)  # Initialize SplashScreen
        self.initialize_ui()

    def initialize_ui(self):
        # Display splash screen initially
        self.splash_screen.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
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
        self.date_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
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

        # Create loading indicator before data is loaded
        self.loading_label = ctk.CTkLabel(self, text="Loading Ingredients...", font=("Arial", 16))
        self.loading_label.grid(row=2, column=0, columnspan=3, pady=20)

        # Load ingredients data immediately, without waiting for the splash screen
        self.load_ingredients_data()  # Immediately load the data
        
        # Use a 2-second delay to hide the splash screen and display the main content
        self.after(500, self.hide_splash_screen)

    def configure_grid(self):
        for column in range(3):
            self.grid_columnconfigure(column, weight=1, uniform="nutrition")
        self.grid_rowconfigure(1, weight=2, minsize=150)  # Adjusted minsize for better display
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=1)

    def load_ingredients_data(self):
        # Load ingredients data and sort it immediately
        self.ingredients_data = load_from_ingredients_json()
        self.sorted_ingredients = sort_ingredients(self.ingredients_data, criteria="frequency_of_use")

        # Proceed to create UI components now that the data is loaded
        self.create_ingredients_frame()  # Replace the old frame with IngredientsFrame
        self.create_bottom_frame()

    def hide_splash_screen(self):
        # Hide the splash screen after 2 seconds
        self.splash_screen.hide()
        self.loading_label.grid_forget()  # Remove the loading label

        # Now delay the creation of progress frames
        self.after(500, self.create_progress_frames)  # Delay creating progress frames

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
        # Use IngredientsFrame instead of the old frame
        self.ingredients_frame = IngredientsFrame(
            master=self,
            ingredients_data=self.sorted_ingredients,
            update_bottom_frame_callback=self.update_bottom_frame,
        )
        self.ingredients_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=0, sticky="nsew")

    def update_bottom_frame(self, ingredients_data, add):
        self.bottom_frame.update_selected_data(ingredients_data, add)

    def create_bottom_frame(self):
        self.bottom_frame = BottomFrame(
            master=self,
            nutrition_view_model=self.nutrition_view_model,
            update_intake_callback=self.update_intake,
            update_cards_callback=self.sort_cards,
            ingredient_cards=self.ingredients_frame.ingredient_cards  # Pass ingredient data to BottomFrame
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
            
    def sort_cards(self, selected_option):
        # Map selected options to the corresponding sorting criteria
        self.ingredients_data = load_from_ingredients_json()
        descending = True
        if selected_option == "Frequency":
            criteria = "frequency_of_use"
        elif selected_option == "Alphabetical":
            criteria = "name"
            descending = False
        elif selected_option == "Recently Used":
            criteria = "last_used_date"
        elif selected_option == "Protein":
            criteria = "protein"
        elif selected_option == "Carbohydrate":
            criteria = "carbohydrate"
        self.ingredients_data = sort_ingredients(self.ingredients_data, criteria, descending)
        self.ingredients_frame.ingredients_data = self.ingredients_data
        self.ingredients_frame.populate_ingredient_cards()  # Re-populate the ingredient cards after sorting