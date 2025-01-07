import customtkinter as ctk
from ttkbootstrap.widgets import Meter


class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master, goal_name, goal_value, consumed_value, update_callback):
        super().__init__(master, fg_color="transparent")

        self.goal_name = goal_name
        self.goal_value = goal_value
        self.consumed_value = consumed_value
        self.update_callback = update_callback

        self.initialize_ui()

    def initialize_ui(self):
        # Label for nutrition goal
        self.label = ctk.CTkLabel(self, text="")
        self.label.pack(pady=5)

        # Create the circular progress bar
        self.progress_bar = self.create_circular_progress_bar()

        # Update the label and progress bar
        self.update_nutrition_label(self.label, self.progress_bar, self.goal_name, self.goal_value, {self.goal_name: self.consumed_value})

    def create_circular_progress_bar(self):
        # Calculate the percentage
        percentage = (self.consumed_value / self.goal_value) * 100 if self.goal_value > 0 else 0

        # Create and style the circular progress bar
        progress_bar = Meter(
            master=self,
            amountused=self.consumed_value,  # Current progress
            amounttotal=self.goal_value,    # Goal value
            metersize=120,                 # Diameter of the circle
            bootstyle="success" if self.goal_name == "protein" else 
                      "warning" if self.goal_name == "carbohydrate" else "danger",  # Colors for different nutrients
            interactive=False,             # Non-interactive
            subtext=f"{round(percentage, 1)}%",  # Display percentage
            textfont=("Arial", 12, "bold"),  # Font for subtext
            textright=False,               # Disable extra text like "x/y"
            padding=10,                    # Add padding for a cleaner look
        )
        progress_bar.pack(expand=True, padx=5, pady=5)
        return progress_bar

    def update(self, nutrition_data):
        consumed_value = nutrition_data.get(self.goal_name, 0)
        self.update_nutrition_label(self.label, self.progress_bar, self.goal_name, self.goal_value, {self.goal_name: consumed_value})

    @staticmethod
    def update_nutrition_label(label, progress_bar, goal_name, goal_value, nutrition_data):
        consumed_value = round(nutrition_data.get(goal_name, 0), 2)
        percentage = min(100, (consumed_value / goal_value) * 100 if goal_value > 0 else 0)

        label.configure(
            text=(
                f"{goal_name.capitalize()} Goal: {goal_value}g\n"
                f"Consumed: {consumed_value}g | {round(percentage, 2)}%"
            )
        )

        progress_bar.configure(
            amountused=consumed_value,
            subtext=f"{round(percentage, 2)}% | {consumed_value}g"
        )
        
    def update_progress_labels(self, nutrition_manager, selected_ingredients):
        nutrition_manager.update_nutrition(selected_ingredients)
        nutrition_data = nutrition_manager.get_nutrition_data()

        self.update(nutrition_data)