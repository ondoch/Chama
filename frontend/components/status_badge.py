from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

STATUS_COLORS = {
    "active": ("#c9f7d9", "#1a7f4e"),
    "onboarding": ("#fbe0c4", "#b35900"),
    "inactive": ("#f0f0f0", "#666666"),
}

class StatusBadge(QWidget):
    def __init__(self, status: str):
        super().__init__()
        self.status = status
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel(self.status)
        self.label.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.label)
        self.setLayout(main_layout)

    def setStylesheet(self):
        bg_color, text_color = STATUS_COLORS.get(
            self.status.lower(), STATUS_COLORS["inactive"]
        )
        self.label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 5px;
                padding: 4px 12px;
                font-weight: 400;
                border: 1px solid {text_color};
            }}
        """)
