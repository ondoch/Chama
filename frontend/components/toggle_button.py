from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPropertyAnimation, QRectF, pyqtProperty, QEasingCurve
from PyQt5.QtGui import QPainter, QColor
from components.style_constants import COLOR_ACCENT_BLUE


class ToggleSwitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(38, 18)
        self.setCursor(Qt.PointingHandCursor)

        self._circle_diameter = 15
        self._margin = (self.height() - self._circle_diameter) / 2

        self._checked = False
        self._circle_pos = self._margin

        self._bg_color_off = QColor("#c0c0c0")
        self._bg_color_on = QColor(f"{COLOR_ACCENT_BLUE}")
        self._circle_color = QColor("#ffffff")

        self.animation = QPropertyAnimation(self, b"circle_pos")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    def mousePressEvent(self, event):
        self.setChecked(not self._checked)

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        self._checked = checked
        start = self._circle_pos
        end = self.width() - self._circle_diameter - self._margin if checked else self._margin
        self.animation.stop()
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()
        self.update()

    def get_circle_pos(self):
        return self._circle_pos

    def set_circle_pos(self, pos):
        self._circle_pos = pos
        self.update()

    circle_pos = pyqtProperty(float, get_circle_pos, set_circle_pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        bg = self._bg_color_on if self._checked else self._bg_color_off
        painter.setBrush(bg)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)

        painter.setBrush(self._circle_color)
        painter.drawEllipse(QRectF(self._circle_pos, self._margin, self._circle_diameter, self._circle_diameter))