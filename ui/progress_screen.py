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
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)  # Protein section
        self.grid_columnconfigure(1, weight=1)  # Carbs section
        self.grid_columnconfigure(2, weight=1)  # Calories section
        self.grid_rowconfigure(1, weight=1)  # For protein, carbs, calories row

        # Protein section
        self.protein_frame = ctk.CTkFrame(self)
        self.protein_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.protein_label = ctk.CTkLabel(self.protein_frame, text=f"Protein Goal: {progress_view_modal.user_profile.goal_protein}g")
        self.protein_label.pack(pady=10)

        # Carbs section
        self.carbs_frame = ctk.CTkFrame(self)
        self.carbs_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.carbs_label = ctk.CTkLabel(self.carbs_frame, text=f"Carbs Goal: {progress_view_modal.user_profile.goal_carbs}g")
        self.carbs_label.pack(pady=10)

        # Calories section
        self.calories_frame = ctk.CTkFrame(self)
        self.calories_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.calories_label = ctk.CTkLabel(self.calories_frame, text=f"Calories Goal: {progress_view_modal.user_profile.goal_calories}")
        self.calories_label.pack(pady=10)

        # Update Goals button below the sections
        self.update_button = ctk.CTkButton(self, text="Update Goals", command=self.update_goals)
        self.update_button.grid(row=2, column=0, columnspan=3, pady=20)

    def update_goals(self):
        print("Update Goals clicked!")
        # Extend functionality as needed