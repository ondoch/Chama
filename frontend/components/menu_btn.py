from typing import Optional

from PyQt5.QtWidgets import QPushButton, QLabel, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from components.style_constants import COLOR_SIDEBAR_HOVER, FONT_FAMILY, COLOR_SIDEBAR_SELECT


class MenuBtn(QPushButton):
    def __init__(self, text: str = "", icon_path: Optional[str] = None,
                 badge: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.icon_path = icon_path
        self.badge_text = badge
        self._badge_label: Optional[QLabel] = None
        self.initUI()

    def initUI(self) -> None:
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(38)

        if self.icon_path:
            self.setIcon(QIcon(self.icon_path))
            self.setIconSize(QSize(18, 18))

        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px 12px;
                border: none;
                border-radius: 4px;
                background: transparent;
                color: #FFFFFF;
                font-size: 13px;
                font-family: {FONT_FAMILY};
            }}
            QPushButton:hover {{
                background: {COLOR_SIDEBAR_HOVER};
            }}
            QPushButton:checked {{
                background: {COLOR_SIDEBAR_SELECT};
                color: #FFFFFF;
                font-weight: 600;
            }}
        """)

        if self.badge_text:
            self._badge_label = QLabel(self.badge_text, self)
            self._badge_label.setStyleSheet("""
                QLabel {
                    background: transparent;
                    color: #8A8F9C;
                    font-size: 12px;
                }
            """)
            self._badge_label.adjustSize()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self._badge_label:
            self._badge_label.move(
                self.width() - self._badge_label.width() - 14,
                (self.height() - self._badge_label.height()) // 2,
            )
