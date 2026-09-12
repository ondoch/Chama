from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from components.style_constants import FONT_FAMILY

DEFAULT_AVATAR_COLORS = [
    "#6b6fd6", "#4a90e2", "#50b87f", "#e2a94a", "#e26b6b",
]


class Avatar(QLabel):

    def __init__(self, text: str = "", image_path: str = None,
                 size: int = 28, bg_color: str = None, parent=None):
        super().__init__(parent)
        self.size = size
        self.bg_color = bg_color or self._color_from_text(text)

        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)

        if image_path:
            self._set_image(image_path)
        else:
            self._set_initials(text)

    def _color_from_text(self, text: str) -> str:
        if not text:
            return DEFAULT_AVATAR_COLORS[0]
        index = sum(ord(c) for c in text) % len(DEFAULT_AVATAR_COLORS)
        return DEFAULT_AVATAR_COLORS[index]

    def _set_initials(self, text: str):
        stripped = (text or "").strip()
        initial = stripped[0].upper() if stripped else "?"
        self.setText(initial)
        self.setStyleSheet(f"""
            background-color: {self.bg_color};
            color: white;
            border-radius: {self.size // 2}px;
            font-family: {FONT_FAMILY};
            font-weight: 600;
            font-size: {max(10, self.size // 2 - 2)}px;
        """)

    def _set_image(self, image_path: str):
        pixmap = QPixmap(image_path).scaled(
            self.size, self.size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )
        self.setPixmap(pixmap)
        self.setStyleSheet(f"border-radius: {self.size // 2}px;")
