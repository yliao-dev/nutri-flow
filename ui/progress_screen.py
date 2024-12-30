
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from viewmodel.progress_viewmodel import ProgressViewModel
from model.progress import NutritionData

class ProgressScreen(QWidget):
    """
    The screen displaying nutrition progress and interaction buttons.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Today's Progress")
        self.view_model = ProgressViewModel()

        layout = QVBoxLayout()

        self.calories_label = QLabel("Calories: 0")
        self.calories_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.calories_label)

        self.protein_label = QLabel("Protein: 0")
        self.protein_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.protein_label)

        self.carbohydrates_label = QLabel("Carbohydrates: 0")
        self.carbohydrates_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.carbohydrates_label)

        self.add_button = QPushButton("Add Progress")
        self.add_button.clicked.connect(self.add_progress)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
        
    def update_labels(self):
        """
        Updates the labels to reflect the current nutrition data.
        """
        data = self.view_model.get_progress_data()
        self.calories_label.setText(f"Calories: {data.calories}")
        self.protein_label.setText(f"Protein: {data.protein}")
        self.carbohydrates_label.setText(f"Carbohydrates: {data.carbohydrates}")

    def add_progress(self):
        """
        Adds progress to the nutrition data and updates the labels.
        """
        data = NutritionData(10, 10, 10)
        self.view_model.add_progress(data)
        self.update_labels()