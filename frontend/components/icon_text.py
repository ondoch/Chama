from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from components.style_constants import FONT_FAMILY, COLOR_TEXT_MUTED


class IconText(QWidget):

    def __init__(self, icon_path: str = None, text: str = "",
                 icon_size: int = 14, text_color: str = COLOR_TEXT_MUTED,
                 spacing: int = 6, parent=None):
        super().__init__(parent)
        self._icon_size = icon_size
        self._text_color = text_color

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing)
        layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.icon_label = QLabel()
        if icon_path:
            self.icon_label.setPixmap(
                QIcon(icon_path).pixmap(QSize(icon_size, icon_size))
            )
        layout.addWidget(self.icon_label)

        self.text_label = QLabel(text)
        self._apply_text_style()
        layout.addWidget(self.text_label)
        layout.addStretch()

    def _apply_text_style(self):
        self.text_label.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            color: {self._text_color};
            font-size: 14px;
        """)

    def set_text(self, text: str):
        self.text_label.setText(text)

    def set_icon(self, icon_path: str):
        self.icon_label.setPixmap(
            QIcon(icon_path).pixmap(QSize(self._icon_size, self._icon_size))
        )
