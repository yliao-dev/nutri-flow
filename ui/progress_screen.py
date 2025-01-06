import customtkinter as ctk
from model.user_profile import NutritionData
from ui.ingredient_card import IngredientCard, load_ingredient_data  # Import the IngredientCard class

class ProgressScreen(ctk.CTkFrame):
    def __init__(self, master, progress_view_model):
        super().__init__(master)

        self.progress_view_model = progress_view_model
        self.ingredients_data = load_ingredient_data()  # Ensure this is called early
        self.user_goals = {
            "protein": self.progress_view_model.user_profile.goal_protein,
            "carbs": self.progress_view_model.user_profile.goal_carbs,
            "calories": self.progress_view_model.user_profile.goal_calories
        }

        self.label = ctk.CTkLabel(self, text="Nutrition Progress", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Configure grid weights for columns
        self.grid_columnconfigure(0, weight=4)  # 80% of the row width for the selectedGoals label
        self.grid_columnconfigure(1, weight=1)  # 20% of the row width for the button

        # Configure row
        self.grid_rowconfigure(1, weight=1)

        # Protein Frame
        self.protein_frame = ctk.CTkFrame(self)
        self.protein_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.protein_label = ctk.CTkLabel(self.protein_frame, text=f"Protein Goal: {self.user_goals['protein']}g | Consumed: 0g | 0.0%")
        self.protein_label.pack(pady=10)

        # Carbs Frame
        self.carbs_frame = ctk.CTkFrame(self)
        self.carbs_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.carbs_label = ctk.CTkLabel(self.carbs_frame, text=f"Carbs Goal: {self.user_goals['carbs']}g | Consumed: 0g | 0.0%")
        self.carbs_label.pack(pady=10)

        # Calories Frame
        self.calories_frame = ctk.CTkFrame(self)
        self.calories_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.calories_label = ctk.CTkLabel(self.calories_frame, text=f"Calories Goal: {self.user_goals['calories']} | Consumed: 0 | 0.0%")
        self.calories_label.pack(pady=10)

        # Ingredients Frame with Scrollable Content
        self.ingredients_frame = ctk.CTkFrame(self)
        self.ingredients_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.canvas = ctk.CTkCanvas(self.ingredients_frame, bg="#ffffff", highlightthickness=3)
        self.canvas.pack(side="top", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.ingredients_frame, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x")
        
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.populate_ingredient_cards()

        # Selected Goals Label (Takes 80% of the row)
        selectData = NutritionData(calories=100, carbohydrates=20, protein=10)
        self.selectedGoals = ctk.CTkLabel(self, text=str(selectData))
        self.selectedGoals.grid(row=3, column=0, padx=10, pady=10)

        # Update Button (Aligned to the right corner of the row)
        self.update_button = ctk.CTkButton(self, text="Update Goals", command=self.update_goals)
        self.update_button.grid(row=3, column=1, padx=10, pady=10)

    def populate_ingredient_cards(self):
        # Loop through the ingredient data and create cards using the 'id' as a reference
        for ingredient in self.ingredients_data:
            ingredient_card = IngredientCard(self.scrollable_frame, ingredient['id'], ingredient)
            ingredient_card.grid(row=0, column=ingredient['id'], padx=5, pady=5, sticky="nsew")

    def update_goals(self):
        print("Update Goals clicked!")
        protein = 20  # Example value
        carbs = 30
        calories = 150
        
        self.progress_view_model.increment_values(protein, carbs, calories)
        self.update_progress_labels()

    def update_progress_labels(self):
        progress = self.progress_view_model.progress_model.calculate_percentage()

        protein_goal = self.progress_view_model.user_profile.goal_protein
        protein_consumed = self.progress_view_model.progress_model.nutrition_data.protein
        protein_percentage = progress['protein']
        self.protein_label.configure(
            text=f"Protein Goal: {protein_goal}g | Consumed: {protein_consumed}g | {protein_percentage:.1f}%"
        )

        carbs_goal = self.progress_view_model.user_profile.goal_carbs
        carbs_consumed = self.progress_view_model.progress_model.nutrition_data.carbohydrates
        carbs_percentage = progress['carbohydrates']
        self.carbs_label.configure(
            text=f"Carbs Goal: {carbs_goal}g | Consumed: {carbs_consumed}g | {carbs_percentage:.1f}%"
        )

        calories_goal = self.progress_view_model.user_profile.goal_calories
        calories_consumed = self.progress_view_model.progress_model.nutrition_data.calories
        calories_percentage = progress['calories']
        self.calories_label.configure(
            text=f"Calories Goal: {calories_goal} | Consumed: {calories_consumed} | {calories_percentage:.1f}%"
        )