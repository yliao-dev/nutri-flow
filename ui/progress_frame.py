import customtkinter as ctk
from ttkbootstrap.widgets import Meter
import time


class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master, goal_name, goal_value, consumed_value, update_callback):
        super().__init__(master, fg_color="transparent")  # Ensure transparent background for the frame

        self.goal_name = goal_name
        self.goal_value = goal_value
        self.consumed_value = consumed_value
        self.update_callback = update_callback

        self.initialize_ui()

    def initialize_ui(self):
        # Label for nutrition goal (make sure the label background is transparent)
        self.label = ctk.CTkLabel(self, text="", fg_color="transparent")  # Set transparent background
        self.label.pack(pady=5)

        # Create the circular progress bar
        self.progress_bar = self.create_circular_progress_bar()

        # Update the label and progress bar
        self.update_nutrition_label(self.label, self.progress_bar, self.goal_name, self.goal_value, {self.goal_name: self.consumed_value})

    def create_circular_progress_bar(self):
        # Calculate the percentage
        percentage = (self.consumed_value / self.goal_value) * 100 if self.goal_value > 0 else 0

        # Set the color based on the goal
        if self.goal_name == "protein":
            bootstyle = "primary"  # Protein color
        elif self.goal_name == "carbohydrate":
            bootstyle = "info"  # Carbohydrate color
        elif self.goal_name == "calories":
            bootstyle = "dark"  # Calories color
        else:
            bootstyle = "light"  # Default gray color if not matching

        # Create and style the circular progress bar using the bootstyle
        progress_bar = Meter(
            master=self,
            amountused=percentage,  # Corrected to use percentage for progress
            amounttotal=100,        # Goal is always 100% (total value should always be 100%)
            metersize=120,          # Diameter of the circle
            bootstyle=bootstyle,    # Use predefined styles
            interactive=False,      
            subtext="COMPLETED",  # Display percentage in the center
            textfont=("Arial", 15, "bold"),  # Font for subtext
            textright="%",           # Remove extra text like "x/y"
            stripethickness=5,
            
        )

        progress_bar.pack(expand=True, padx=5, pady=5)
        return progress_bar

    def update(self, nutrition_data):
        consumed_value = nutrition_data.get(self.goal_name, 0)
        self.update_nutrition_label(self.label, self.progress_bar, self.goal_name, self.goal_value, {self.goal_name: consumed_value})

    @staticmethod
    def update_nutrition_label(label, progress_bar, goal_name, goal_value, nutrition_data):
        consumed_value = round(nutrition_data.get(goal_name, 0), 2)
        # Calculate percentage correctly
        percentage = min(100, (consumed_value / goal_value) * 100 if goal_value > 0 else 0)

        label.configure(
            text=(
                f"{goal_name.capitalize()} Goal: {goal_value}g\n"
                f"Consumed: {consumed_value}g | {round(percentage, 2)}%"
            ),
        )

        # Update progress bar with the percentage
        progress_bar.configure(
            amountused=round(percentage, 2),  # Set the amount used as percentage
        )
        
    def update_progress_labels(self, nutrition_manager, selected_ingredients):
        nutrition_manager.update_nutrition(selected_ingredients)
        nutrition_data = nutrition_manager.get_nutrition_data()

        self.update(nutrition_data)
        