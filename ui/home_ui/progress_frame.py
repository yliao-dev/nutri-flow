import customtkinter as ctk
from ui.home_ui.circular_progress_bar import CircularProgressBar  # Assuming this is correct

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master, goal_name, goal_values, consumed_value=None, update_callback=None):
        super().__init__(master)
        
        self.consumed_value = consumed_value if consumed_value else {"consumed_protein": 0, "consumed_carbohydrate": 0, "consumed_fat": 0}
        self.goal_name = goal_name
        self.goal_values = goal_values
        self.update_callback = update_callback
        
        self.PROTEIN_COLOR = "#025d93"
        self.CARBOHYDRATE_COLOR = "#f9d77c"
        self.FAT_COLOR = "#86f4ee"
        
        self.initialize_ui()

    def initialize_ui(self):
        # Goal label
        self.goal_label = ctk.CTkLabel(self, text="")
        self.goal_label.pack(pady=5)

        # Consumed value label
        self.consumed_label = ctk.CTkLabel(self, text="")
        self.consumed_label.pack(pady=5)
        
        # Create a circular progress bar for the goal nutrient
        self.progress_bar = self.create_circular_progress_bar(self.goal_name)
        self.update()

    def create_circular_progress_bar(self, nutrient):
        """Create and return a single circular progress bar for the specified nutrient."""
        colors = {
            "protein": self.PROTEIN_COLOR,
            "carbohydrate": self.CARBOHYDRATE_COLOR,
            "fat": self.FAT_COLOR
        }
        
        progress = (self.consumed_value.get(nutrient, 0) / self.goal_values.get(nutrient, 1)) * 100
        
        progress_bar = CircularProgressBar(
            master=self,
            size=150,
            progress=progress,
            thickness=3,
            color=colors.get(nutrient, "#000000"),
            text_color="white"
        )
        progress_bar.pack(pady=10)
        return progress_bar

    def update(self, nutrition_data=None):
        """Update the progress bar and labels based on new data."""
        if nutrition_data:
            self.consumed_value.update(nutrition_data)

        percentage = round(self.calculate_percentage(self.goal_name), 2)
        self.progress_bar.animate_progress(percentage)
        self.update_nutrition_label()

    def calculate_percentage(self, goal_name):
        """Calculate the percentage progress for the given goal_name."""
        consumed_value = round(self.consumed_value.get(f"consumed_{goal_name}", 0), 2)
        goal_value = self.goal_values.get(goal_name, 1)
        return min(100, (consumed_value / goal_value) * 100 if goal_value > 0 else 0)

    def update_nutrition_label(self):
        """Update the nutrition label and progress bar."""
        # Get the consumed value for the specific goal
        consumed_value = round(self.consumed_value.get(f"consumed_{self.goal_name}", 0), 2)
        # Get the goal value for the specific goal
        goal_value = self.goal_values.get(self.goal_name, 0)
        
        # Calculate the progress percentage using the updated method
        percentage = self.calculate_percentage(self.goal_name)
        
        # Format the labels
        goal_label_text = f"{self.goal_name.capitalize()} Goal: {goal_value}g"
        consumed_label_text = f"Consumed: {consumed_value}g | {round(percentage, 2)}%"
        
        # Apply different font and size for each label
        self.goal_label.configure(text=goal_label_text, font=("Arial", 16, "bold"))
        self.consumed_label.configure(text=consumed_label_text, font=("Arial", 14))