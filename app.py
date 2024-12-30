"""
This module contains the main window for the NutriFlow application.
It sets up the UI with a ProgressScreen to track nutrition progress.
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.progress_screen import ProgressScreen

class MainWindow(QMainWindow): 
    """
    The main application window for NutriFlow.

    This window serves as the central interface for the application,
    displaying the progress screen and handling user interactions.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NutriFlow")
        self.setGeometry(100, 100, 800, 600)

        self.progress_screen = ProgressScreen()
        self.setCentralWidget(self.progress_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())