"""
This module contains the main window for the NutriFlow application.
It sets up the UI with a ProgressScreen to track nutrition progress.
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.progress_screen import ProgressScreen

class MainWindow(QMainWindow):  # Inherit from QMainWindow
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NutriFlow")
        self.setGeometry(100, 100, 800, 600)

        # Add the ProgressScreen as the central widget
        self.progress_screen = ProgressScreen()  # Make sure ProgressScreen is properly imported and defined
        self.setCentralWidget(self.progress_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())