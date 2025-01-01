from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from viewmodal.progress_viewmodal import ProgressViewModal
from modal.progress_modal import NutritionData
from ui.circular_bar import CircularProgressBar

class ProgressScreen(QWidget):
    def __init__(self, view_modal: ProgressViewModal):
        super().__init__()

        self.setWindowTitle("Today's Progress")
        self.view_modal = view_modal

        layout = QVBoxLayout()

        self.progress_label = QLabel("Today's Progress")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_label)

        # User profile data
        self.weight_label = QLabel(f"Weight: {self.view_modal.modal.user_profile.weight} kg")
        self.goal_protein_label = QLabel(f"Goal Protein: {self.view_modal.modal.user_profile.goal_protein} g")
        self.goal_carbs_label = QLabel(f"Goal Carbs: {self.view_modal.modal.user_profile.goal_carbs} g")
        self.goal_calories_label = QLabel(f"Goal Calories: {self.view_modal.modal.user_profile.goal_calories} kcal")
        
        for label in [self.weight_label, self.goal_protein_label, self.goal_carbs_label, self.goal_calories_label]:
            layout.addWidget(label)

        # Circular progress bars for Protein, Carbs, and Calories
        self.protein_progress = CircularProgressBar(self)
        self.carbs_progress = CircularProgressBar(self)
        self.calories_progress = CircularProgressBar(self)

        # Configure progress bar settings
        for progress_bar in [self.protein_progress, self.carbs_progress, self.calories_progress]:
            progress_bar.setMaximum(100)  # Set max percentage
            progress_bar.setFixedSize(150, 150)  # Set size of the progress bar

        # Add progress bars to the layout
        layout.addWidget(self.protein_progress)
        layout.addWidget(self.carbs_progress)
        layout.addWidget(self.calories_progress)

        # Button to add progress
        self.add_button = QPushButton("Add Progress")
        self.add_button.clicked.connect(self.add_progress)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_progress(self):
        """Adds progress to nutrition data and updates the labels."""
        nutrition_data = NutritionData(calories=10, protein=10, carbohydrates=10)
        self.view_modal.add_progress(nutrition_data)

        # Update the circular progress bars and labels
        self.update_progress_bars()

    def update_progress_bars(self):
        nutrition_data = self.view_modal.get_progress_data()
        percentage = self.view_modal.calculate_percentage()

        # Update each progress bar with the corresponding percentage
        self.protein_progress.setValue(percentage['protein'])
        self.carbs_progress.setValue(percentage['carbohydrates'])
        self.calories_progress.setValue(percentage['calories'])

        # Add text to show the values in the center of the circular bars (optional)
        self.protein_progress.setText(f"Protein: {percentage['protein']:.2f}%")
        self.carbs_progress.setText(f"Carbs: {percentage['carbohydrates']:.2f}%")
        self.calories_progress.setText(f"Calories: {percentage['calories']:.2f}%")