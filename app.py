"""
Main entry point for the NutriFlow application.
This file initializes the application, creates the main window, and displays the progress screen.
"""
import sys
from PyQt5.QtWidgets import QApplication
from ui.progress_screen import ProgressScreen



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NutriFlow")
        self.setGeometry(100, 100, 800, 600)

        # Add the ProgressScreen as the central widget
        self.progress_screen = ProgressScreen()
        self.setCentralWidget(self.progress_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())