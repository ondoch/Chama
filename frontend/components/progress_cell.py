from PyQt5.QtCore import Qt, QRectF, QSize
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtWidgets import QSizePolicy, QWidget


class ProgressCell(QWidget):
    TRACK = QColor("#E5E7EB")
    TEXT = QColor("#374151")
    GREEN = QColor("#1FA35B")
    BLUE = QColor("#2F5BEA")
    AMBER = QColor("#F5A623")

    BAR_HEIGHT = 8
    TEXT_WIDTH = 42
    SIDE_MARGIN = 8

    def __init__(self, value=0, parent=None):
        super().__init__(parent)
        self._value = 0
        self.setMinimumHeight(24)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.set_value(value)

    def set_value(self, value):
        try:
            number = int(round(float(value)))
        except (TypeError, ValueError):
            number = 0
        self._value = max(0, min(100, number))
        self.setToolTip(f"{self._value}% complete")
        self.update()

    def value(self):
        return self._value

    @classmethod
    def color_for(cls, value):
        if value >= 80:
            return cls.GREEN
        if value >= 50:
            return cls.BLUE
        return cls.AMBER

    def sizeHint(self):
        return QSize(150, 28)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        m = self.SIDE_MARGIN
        bar_w = max(20.0, self.width() - self.TEXT_WIDTH - 2 * m)
        bar_y = (self.height() - self.BAR_HEIGHT) / 2
        radius = self.BAR_HEIGHT / 2

        track = QRectF(m, bar_y, bar_w, self.BAR_HEIGHT)
        p.setPen(Qt.NoPen)
        p.setBrush(self.TRACK)
        p.drawRoundedRect(track, radius, radius)

        if self._value > 0:
            fill = QRectF(m, bar_y, max(self.BAR_HEIGHT, bar_w * self._value / 100),
                          self.BAR_HEIGHT)
            p.setBrush(self.color_for(self._value))
            p.drawRoundedRect(fill, radius, radius)

        font = QFont(self.font())
        font.setPixelSize(13)
        font.setBold(True)
        p.setFont(font)
        p.setPen(self.TEXT)
        p.drawText(QRectF(m + bar_w + 6, 0, self.TEXT_WIDTH, self.height()),
                   Qt.AlignLeft | Qt.AlignVCenter, f"{self._value}%")
        p.end()
