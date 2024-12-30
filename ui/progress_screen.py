from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from viewmodal.progress_viewmodal import ProgressViewModal
from modal.progress_modal import NutritionData

class ProgressScreen(QWidget):
    def __init__(self, view_modal: ProgressViewModal):
        super().__init__()

        self.setWindowTitle("Today's Progress")
        self.view_modal = view_modal

        layout = QVBoxLayout()

        self.progress_label = QLabel("Today's Progress")
        self.progress_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_label)


        self.weight_label = QLabel(f"Weight: {self.view_modal.modal.user_profile.weight} kg")
        self.goal_protein_label = QLabel(f"Goal Protein: {self.view_modal.modal.user_profile.goal_protein} g")
        self.goal_carbs_label = QLabel(f"Goal Carbs: {self.view_modal.modal.user_profile.goal_carbs} g")
        self.goal_calories_label = QLabel(f"Goal Calories: {self.view_modal.modal.user_profile.goal_calories} kcal")
        
        for label in [self.weight_label, self.goal_protein_label, self.goal_carbs_label, self.goal_calories_label]:
            layout.addWidget(label)
        # Labels for displaying the progress
       
        self.protein_label = QLabel(f"Protein: 0 g")
        self.carbs_label = QLabel(f"Carbs: 0 g")
        self.calories_label = QLabel(f"Calories: 0 kcal")


        # Add all labels to layout
        for label in [self.protein_label, self.carbs_label, self.calories_label]:
            layout.addWidget(label)

        self.add_button = QPushButton("Add Progress")
        self.add_button.clicked.connect(self.add_progress)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_progress(self):
        """Adds progress to nutrition data and updates the labels."""
        # Example: Add progress with 10 calories, protein, and carbs
        nutrition_data = NutritionData(calories=10, protein=10, carbohydrates=10)
        self.view_modal.add_progress(nutrition_data)

        # Update the labels with current intake and percentages
        self.update_labels()

    def update_labels(self):
        nutrition_data = self.view_modal.get_progress_data()
        percentage = self.view_modal.calculate_percentage()

        # Format and update each label with both percentage and current intake
        self._update_label(self.protein_label, 
                        f"Protein: {percentage['protein']:.2f}% ({nutrition_data.protein} g)")
        self._update_label(self.carbs_label, 
                        f"Carbs: {percentage['carbohydrates']:.2f}% ({nutrition_data.carbohydrates} g)")
        self._update_label(self.calories_label, 
                        f"Calories: {percentage['calories']:.2f}% ({nutrition_data.calories} kcal)")

    def _update_label(self, label, text):
        """Helper function to update the text of a label."""
        label.setText(text)