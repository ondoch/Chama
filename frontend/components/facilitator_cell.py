from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget

from components.style_constants import (
    FONT_FAMILY,
)

class Avatar(QWidget):
    PALETTE = ["#2F5BEA", "#1FA35B", "#F5A623", "#E5484D", "#8B5CF6", "#0EA5C6"]

    def __init__(self, name="", avatar_path=None, size=30, parent=None):
        super().__init__(parent)
        self._name = name or ""
        self._pixmap = None
        if avatar_path:
            pix = QPixmap(avatar_path)
            if not pix.isNull():
                self._pixmap = pix
        self.setFixedSize(size, size)

    def _initials(self):
        parts = self._name.split()
        if not parts:
            return "?"
        letters = parts[0][0] + (parts[1][0] if len(parts) > 1 else "")
        return letters.upper()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        rect = QRectF(self.rect())

        clip = QPainterPath()
        clip.addEllipse(rect)
        p.setClipPath(clip)

        if self._pixmap is not None:
            scaled = self._pixmap.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            x = (scaled.width() - self.width()) // 2
            y = (scaled.height() - self.height()) // 2
            p.drawPixmap(0, 0, scaled, x, y, self.width(), self.height())
        else:
            color = self.PALETTE[sum(map(ord, self._name)) % len(self.PALETTE)]
            p.fillRect(rect, QColor(color))
            font = QFont(self.font())
            font.setBold(True)
            font.setPixelSize(int(self.height() * 0.40))
            p.setFont(font)
            p.setPen(QColor("white"))
            p.drawText(rect, Qt.AlignCenter, self._initials())
        p.end()


class FacilitatorCell(QWidget):
    def __init__(self, name="", avatar_path=None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(10)

        self.avatar = Avatar(name, avatar_path)
        self.label = QLabel(name or "-")
        self.label.setStyleSheet(
            f"color: #1F2937; font-size: 12px; ; font-family: {FONT_FAMILY}; background: transparent; border: none;"
        )
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)

        layout.addWidget(self.avatar, 0, Qt.AlignVCenter)
        layout.addWidget(self.label, 1, Qt.AlignVCenter)
