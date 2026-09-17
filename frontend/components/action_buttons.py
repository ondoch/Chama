from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

BUTTON_STYLE = """
    QPushButton {
        border-radius: 5px;
        border: 1px solid #ccc;
        background-color: #ffffff;
    }
    QPushButton:hover {
        background-color: #f5f5f5;
    }
"""


class ActionButtonGroup(QWidget):
    def __init__(self, actions: list, row_data=None,
                 button_size: int = 30, spacing: int = 6, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing)
        layout.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)

        for action in actions:
            btn = QPushButton(action.get("label", ""))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(BUTTON_STYLE)

            if action.get("icon"):
                btn.setIcon(QIcon(action["icon"]))
                btn.setIconSize(QSize(14, 14))
                btn.setFixedSize(button_size, button_size)
            else:
                btn.setFixedHeight(button_size)
                btn.setFixedWidth(action.get("width", button_size * 2))

            callback = action.get("callback")
            if callback:
                btn.clicked.connect(lambda _checked, cb=callback, b=btn: cb(row_data, b))

            layout.addWidget(btn)