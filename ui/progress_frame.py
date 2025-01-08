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
        
        # Create circular progress bars for each nutrient
        self.progress_bars = self.create_circular_progress_bars()
        
        # Update nutrition labels
        self.update_nutrition_label(self.label, self.progress_bars)

    def create_circular_progress_bars(self):
        """Create and return 3 circular progress bars for protein, carbs, and calories."""
        progress_bars = {}
        nutrients = ["protein", "carbohydrate", "calories"]
        colors = [self.PROTEIN_COLOR, self.CARBOHYDRATE_COLOR, self.CALORIES_COLOR]
        print(self.consumed_value)
        for nutrient, color in zip(nutrients, colors):
            # Calculate the progress percentage for each nutrient
            progress = (self.consumed_value[nutrient] / self.goal_values[nutrient]) * 100
            progress_bars[nutrient] = CircularProgressBar(
                master=self,
                size=150,
                progress=progress,
                thickness=3,
                color=color,
                bg_color="transparent",
                text_color="white"
            )
            progress_bars[nutrient].pack(side="left", padx=10)

        return progress_bars

    def update(self, nutrition_data):
        """Update the progress bars and labels based on new data."""
        self.consumed_value.update(nutrition_data)
        self.update_nutrition_label(self.label, self.progress_bars)

    def update_nutrition_label(self, label, progress_bars):
        """Update the nutrition label and progress bars."""
        label_text = ""
        for nutrient in self.consumed_value:
            consumed_value = round(self.consumed_value[nutrient], 2)
            goal_value = self.goal_values.get(nutrient, 0)
            percentage = min(100, (consumed_value / goal_value) * 100 if goal_value > 0 else 0)
            
            label_text += f"{nutrient.capitalize()} Goal: {goal_value}g\n"
            label_text += f"Consumed: {consumed_value}g | {round(percentage, 2)}%\n\n"
            
            # Update each progress bar
            progress_bars[nutrient].update_progress(round(percentage, 2))

        label.configure(text=label_text)