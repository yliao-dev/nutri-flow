"""
This module contains the main window for the NutriFlow application.
It sets up the UI with a ProgressScreen to track nutrition progress.
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.progress_screen import ProgressScreen
from viewmodal.progress_viewmodal import ProgressViewModal
from modal.user_profile import UserProfile

class MainWindow(QMainWindow): 
    """
    The main application window for NutriFlow.

    This window serves as the central interface for the application,
    displaying the progress screen and handling user interactions.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NutriFlow")
        self.setGeometry(100, 200, 700, 600)
        user_profile = UserProfile(weight=70, goal_protein=150, goal_carbs=200, goal_calories=2500)
        self.progress_view_modal = ProgressViewModal(user_profile)
        self.progress_screen = ProgressScreen(self.progress_view_modal)
        self.setCentralWidget(self.progress_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())