import customtkinter as ctk
from ui.circular_progress_bar import CircularProgressBar  # Assuming you have this imported correctly

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master, goal_name, goal_values, consumed_value=None, update_callback=None):
        super().__init__(master)
        
        # Set default consumed value to 0 if None provided
        self.consumed_value = consumed_value if consumed_value else {"protein": 0, "carbohydrate": 0, "calories": 0}
        self.goal_name = goal_name
        self.goal_values = goal_values  # Dictionary of goal values for each nutrient
        self.update_callback = update_callback  # Callback for updates
        
        # Define colors for each nutrient
        self.PROTEIN_COLOR = "#025d93"
        self.CARBOHYDRATE_COLOR = "#f9d77c"
        self.CALORIES_COLOR = "#977a68"
        
        # Initialize UI components
        self.initialize_ui()

    def initialize_ui(self):
        self.label = ctk.CTkLabel(self, text="")
        self.label.pack(pady=5)
        
        # Create a single circular progress bar for the goal nutrient
        self.progress_bar = self.create_circular_progress_bar(self.goal_name)  # Pass the goal_name here
        
        # Update nutrition labels
        self.update_nutrition_label(self.label, self.progress_bar)

    def create_circular_progress_bar(self, nutrient):
        """Create and return a single circular progress bar for the specified nutrient."""
        colors = {
            "protein": self.PROTEIN_COLOR,
            "carbohydrate": self.CARBOHYDRATE_COLOR,
            "calories": self.CALORIES_COLOR
        }
        
        # Calculate the progress percentage for the specified nutrient
        progress = (self.consumed_value.get(nutrient, 0) / self.goal_values.get(nutrient, 1)) * 100
        
        return CircularProgressBar(
            master=self,
            size=150,
            progress=progress,
            thickness=3,
            color=colors.get(nutrient, "#000000"),  # Default to black if nutrient not found
            bg_color="transparent",
            text_color="white"
        )

    def update(self, nutrition_data):
        """Update the progress bar and labels based on new data."""
        self.consumed_value.update(nutrition_data)
        self.update_nutrition_label(self.label, self.progress_bar)

    def update_nutrition_label(self, label, progress_bar):
        """Update the nutrition label and progress bar."""
        consumed_value = round(self.consumed_value.get(self.goal_name, 0), 2)
        goal_value = self.goal_values.get(self.goal_name, 0)
        percentage = min(100, (consumed_value / goal_value) * 100 if goal_value > 0 else 0)
        
        label_text = f"{self.goal_name.capitalize()} Goal: {goal_value}g\n"
        label_text += f"Consumed: {consumed_value}g | {round(percentage, 2)}%\n"
        
        # Update the progress bar
        progress_bar.update_progress(round(percentage, 2))
        
        label.configure(text=label_text)