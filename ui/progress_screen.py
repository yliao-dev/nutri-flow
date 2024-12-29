# ui/progress_screen.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class ProgressScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Today's Progress")

        # Layout to hold widgets
        layout = QVBoxLayout()

        # Add a label for today's progress
        self.progress_label = QLabel("Today's Progress")
        self.progress_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_label)

        # Add a button to simulate adding progress
        self.add_button = QPushButton("Add Progress")
        self.add_button.clicked.connect(self.add_progress)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_progress(self):
        # Here, you can implement the logic to update the progress
        print("Progress Added!")
        self.progress_label.setText("Progress Updated!")