from PyQt5.QtWidgets import QFrame, QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from components.style_constants import FONT_FAMILY, COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED, COLOR_ACCENT_BLUE, COLOR_ACCENT_BLUE_BG


class Description(QFrame):
    def __init__(self, number, title, description):
        super().__init__()
        self.number = number
        self.title = title
        self.description = description
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        self.setObjectName("step_row")
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(4, 8, 4, 8)
        main_layout.setSpacing(14)
        main_layout.setAlignment(Qt.AlignTop)

        number_label = QLabel(str(self.number))
        number_label.setObjectName("number_label")
        number_label.setAlignment(Qt.AlignCenter)
        number_label.setFixedSize(30, 30)

        sub_layout = QVBoxLayout()
        sub_layout.setSpacing(2)
        sub_layout.setContentsMargins(0, 2, 0, 0)

        description_1 = QLabel(self.title)
        description_1.setObjectName("description_1")
        description_2 = QLabel(self.description)
        description_2.setObjectName("description_2")
        description_2.setWordWrap(True)

        sub_layout.addWidget(description_1)
        sub_layout.addWidget(description_2)

        main_layout.addWidget(number_label)
        main_layout.addLayout(sub_layout)
        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QFrame#step_row {{
                background-color: transparent;
                border-radius: 8px;
            }}
            QLabel#number_label {{
                border-radius: 15px;
                background-color: {COLOR_ACCENT_BLUE_BG};
                color: {COLOR_ACCENT_BLUE};
                font-family: '{FONT_FAMILY}';
                font-size: 14px;
                font-weight: 600;
            }}
            QLabel#description_1 {{
                font-family: '{FONT_FAMILY}';
                font-size: 14px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#description_2 {{
                font-family: '{FONT_FAMILY}';
                font-size: 13px;
                font-weight: 400;
                color: {COLOR_TEXT_MUTED};
                background-color: transparent;
            }}
        """)