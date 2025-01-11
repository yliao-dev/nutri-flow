import customtkinter as ctk
from ui.progress_frame import ProgressFrame
from ui.ingredient_card import IngredientCard, load_ingredient_data
from ui.bottom_frame import BottomFrame


class HomeScreen(ctk.CTkFrame):
    def __init__(self, master, progress_view_model):
        super().__init__(master)

        self.progress_view_model = progress_view_model
        self.nutrition_manager = self.progress_view_model.nutrition_manager
        self.ingredients_data = load_ingredient_data()
        self.user_goals = {
            "protein": self.progress_view_model.user_profile.goal_protein,
            "carbohydrate": self.progress_view_model.user_profile.goal_carbs,
            "calories": self.progress_view_model.user_profile.goal_calories,
        }

        self.progress_frames = {}  # Dictionary to store the progress frames
        self.ingredient_cards = []  # List to store IngredientCard instances

        self.initialize_ui()

    def initialize_ui(self):
        self.label = ctk.CTkLabel(self, text="Nutrition Progress", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.configure_grid()
        self.create_progress_frames()
        self.create_ingredients_frame()
        self.populate_ingredient_cards()
        self.create_bottom_frame()

    def configure_grid(self):
        for column in range(3):
            self.grid_columnconfigure(column, weight=1, uniform="nutrition")
        self.grid_rowconfigure(1, weight=3, minsize=150)  # Adjusted minsize for better display
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=1)

    def create_progress_frames(self):
        goal_names = ["protein", "carbohydrate", "calories"]
        consumed_values = self.nutrition_manager.get_nutrition_data()
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
        self.ingredients_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.canvas = ctk.CTkCanvas(self.ingredients_frame, highlightthickness=3)
        self.canvas.pack(side="top", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.ingredients_frame, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def populate_ingredient_cards(self):
        for ingredient in self.ingredients_data:
            ingredient_card = IngredientCard(self.scrollable_frame, ingredient["id"], ingredient, self.update_bottom_frame)
            ingredient_card.grid(row=0, column=ingredient["id"], padx=5, pady=5, sticky="nsew")
            self.ingredient_cards.append(ingredient_card)

    def update_bottom_frame(self, ingredient_data, add):
        self.bottom_frame.update_selected_data(ingredient_data, add)

    def create_bottom_frame(self):
        self.bottom_frame = BottomFrame(
            master=self,
            nutrition_manager=self.nutrition_manager,
            update_intake_callback=self.update_intake,
            ingredient_cards=self.ingredient_cards,
        )
        self.bottom_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def update_intake(self, nutrition_data):
        # Update each progress frame with the new data
        for _, progress_frame in self.progress_frames.items():
            progress_frame.update(nutrition_data)