import customtkinter as ctk

class ProgressScreen(ctk.CTkFrame):
    """
    The main screen for tracking nutrition progress.
    """
    def __init__(self, master, progress_view_model):
        super().__init__(master)

        self.progress_view_model = progress_view_model

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Nutrition Progress", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)  # Protein section
        self.grid_columnconfigure(1, weight=1)  # Carbs section
        self.grid_columnconfigure(2, weight=1)  # Calories section
        self.grid_rowconfigure(1, weight=1)  # For protein, carbs, calories row

        # Protein section
        self.protein_frame = ctk.CTkFrame(self)
        self.protein_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.protein_label = ctk.CTkLabel(self.protein_frame, text="Protein Goal: 0g")
        self.protein_label.pack(pady=10)

        # Carbs section
        self.carbs_frame = ctk.CTkFrame(self)
        self.carbs_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.carbs_label = ctk.CTkLabel(self.carbs_frame, text="Carbs Goal: 0g")
        self.carbs_label.pack(pady=10)

        # Calories section
        self.calories_frame = ctk.CTkFrame(self)
        self.calories_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.calories_label = ctk.CTkLabel(self.calories_frame, text="Calories Goal: 0")
        self.calories_label.pack(pady=10)

        # Update Goals button below the sections
        self.update_button = ctk.CTkButton(self, text="Update Goals", command=self.update_goals)
        self.update_button.grid(row=2, column=0, columnspan=3, pady=20)

    def update_goals(self):
        """
        Update the nutrition data when the button is clicked.
        """
        print("Update Goals clicked!")

        # Example data for consumed nutrition (can be dynamic)
        protein = 20  # Update with real data
        carbs = 30
        calories = 150
        
        # Increment values in ViewModel (which updates Model)
        self.progress_view_model.increment_values(protein, carbs, calories)

        # Update the labels to reflect new progress
        self.update_progress_labels()

    def update_progress_labels(self):
        """
        Update the progress labels with new values.
        """
        # Get the progress percentages for each nutrient
        progress = self.progress_view_model.progress_model.calculate_percentage()

        # Protein label update
        protein_goal = self.progress_view_model.user_profile.goal_protein
        protein_consumed = self.progress_view_model.progress_model.nutrition_data.protein
        protein_percentage = progress['protein']
        self.protein_label.configure(
            text=f"Protein Goal: {protein_goal}g | Consumed: {protein_consumed}g | {protein_percentage:.1f}%"
        )

        # Carbs label update
        carbs_goal = self.progress_view_model.user_profile.goal_carbs
        carbs_consumed = self.progress_view_model.progress_model.nutrition_data.carbohydrates
        carbs_percentage = progress['carbohydrates']
        self.carbs_label.configure(
            text=f"Carbs Goal: {carbs_goal}g | Consumed: {carbs_consumed}g | {carbs_percentage:.1f}%"
        )

        # Calories label update
        calories_goal = self.progress_view_model.user_profile.goal_calories
        calories_consumed = self.progress_view_model.progress_model.nutrition_data.calories
        calories_percentage = progress['calories']
        self.calories_label.configure(
            text=f"Calories Goal: {calories_goal} | Consumed: {calories_consumed} | {calories_percentage:.1f}%"
        )