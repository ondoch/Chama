from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from components.style_constants import COLOR_BORDER

class PasswordFormInput(QFrame):
    def __init__(self, header, show_icon_path=None, hide_icon_path=None):
        super().__init__()
        self.header = header
        self.show_icon_path = show_icon_path
        self.hide_icon_path = hide_icon_path
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(4)

        header = QLabel(self.header)

        self.entry = QLineEdit()
        self.entry.setEchoMode(QLineEdit.Password)
        self.entry.setFixedHeight(40)

        self.toggle_btn = QPushButton(self.entry)
        self.toggle_btn.setObjectName("toggleBtn")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setFocusPolicy(Qt.NoFocus)

        has_icons = bool(self.show_icon_path and self.hide_icon_path)
        self.toggle_btn.setFixedSize(30 if has_icons else 46, 30)
        self.toggle_btn.setIconSize(QSize(18, 18))
        self.toggle_btn.setToolTip("Show password")
        self.toggle_btn.toggled.connect(self.toggle_password_visibility)
        self._update_toggle_icon(False)

        entry_layout = QHBoxLayout(self.entry)
        entry_layout.setContentsMargins(0, 0, 5, 0)
        entry_layout.addStretch()
        entry_layout.addWidget(self.toggle_btn)

        padding_right = 35 if has_icons else 52
        self.entry.setTextMargins(0, 0, padding_right, 0)

        main_layout.addWidget(header)
        main_layout.addWidget(self.entry)

    def toggle_password_visibility(self, checked):
        self.entry.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)
        self.toggle_btn.setToolTip("Hide password" if checked else "Show password")
        self._update_toggle_icon(checked)
        self.entry.setFocus()

    def _update_toggle_icon(self, visible):
        path = self.hide_icon_path if visible else self.show_icon_path
        if path:
            self.toggle_btn.setText("")
            self.toggle_btn.setIcon(QIcon(path))
        else:
            self.toggle_btn.setIcon(QIcon())
            self.toggle_btn.setText("Hide" if visible else "Show")

    def returnValue(self):
        return self.entry.text()

    def isEmpty(self):
        return self.entry.text().strip() == ""

    def setError(self, has_error):
        border_color = "#e53935" if has_error else COLOR_BORDER
        self.entry.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {border_color};
                background: transparent;
                font-size: 12px;
                font-family: Arial, sans-serif;
                border-radius: 5px;
                padding-left: 5px;
            }}
            QPushButton#toggleBtn {{
                border: none;
                background: transparent;
                font-size: 11px;
                color: #6B7280;
            }}
            QPushButton#toggleBtn:hover {{
                background-color: #F0F2F4;
                border-radius: 4px;
            }}
        """)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: transparent;
            }}
            QLabel {{
                border: none;
                background: transparent;
                font-size: 12px;
                font-family: Arial, sans-serif;
            }}
            QLineEdit {{
                border: 1px solid {COLOR_BORDER};
                background: transparent;
                font-size: 12px;
                font-family: Arial, sans-serif;
                border-radius: 5px;
                padding-left: 5px;
            }}
            QPushButton#toggleBtn {{
                border: none;
                background: transparent;
                font-size: 11px;
                color: #6B7280;
            }}
            QPushButton#toggleBtn:hover {{
                background-color: #F0F2F4;
                border-radius: 4px;
            }}
        """)
