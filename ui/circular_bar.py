from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor

class CircularProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.maximum = 100
        self.size = 150
        self.text = ""

    def setValue(self, value: int):
        self.value = value
        self.update()

    def setMaximum(self, maximum: int):
        self.maximum = maximum

    def setText(self, text: str):
        """Set text to be displayed inside the progress circle."""
        self.text = text
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle background
        painter.setBrush(QColor(240, 240, 240))
        painter.drawEllipse(10, 10, self.size - 20, self.size - 20)

        # Draw progress circle
        painter.setBrush(QColor(0, 128, 255))
        painter.setPen(Qt.PenStyle.NoPen)
        start_angle = 90 * 16
        span_angle = int((self.value / self.maximum) * 360 * 16)  # Cast to int
        painter.drawArc(10, 10, self.size - 20, self.size - 20, start_angle, span_angle)

        # Draw text in the center
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text)