import customtkinter as ctk


class ProgressScreen(ctk.CTkFrame):
    """
    The main screen for tracking nutrition progress.
    """
    def __init__(self, master, progress_view_modal):
        super().__init__(master)

        self.progress_view_modal = progress_view_modal

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Nutrition Progress", font=("Arial", 20, "bold"))
        self.label.pack(pady=10)

        self.protein_label = ctk.CTkLabel(self, text=f"Protein Goal: {progress_view_modal.user_profile.goal_protein}g")
        self.protein_label.pack(pady=5)

        self.carbs_label = ctk.CTkLabel(self, text=f"Carbs Goal: {progress_view_modal.user_profile.goal_carbs}g")
        self.carbs_label.pack(pady=5)

        self.calories_label = ctk.CTkLabel(self, text=f"Calories Goal: {progress_view_modal.user_profile.goal_calories}")
        self.calories_label.pack(pady=5)

        # Example button (extend as needed)
        self.update_button = ctk.CTkButton(self, text="Update Goals", command=self.update_goals)
        self.update_button.pack(pady=10)

    def update_goals(self):
        print("Update Goals clicked!")
        # Extend functionality as needed