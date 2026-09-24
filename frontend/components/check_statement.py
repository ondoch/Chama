from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QSizePolicy,
    QHBoxLayout,
    QVBoxLayout,
    QCheckBox
)

from components.style_constants import (
    FONT_FAMILY,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    COLOR_ACCENT_BLUE,
    COLOR_ACCENT_BLUE_BG,
    COLOR_CARD_BG,
    COLOR_BORDER
)

class CheckStatement(QFrame):
    def __init__(self, header, description):
        super().__init__()

        self.header_text = header
        self.description_text = description

        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        container_widget = QWidget()
        container_widget.setMinimumHeight(80)
        container_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Minimum
        )
        container_widget.setObjectName("container")

        container_layout = QHBoxLayout(container_widget)
        container_layout.setContentsMargins(14, 5, 5, 5)
        container_layout.setSpacing(12)

        self.check_box = QCheckBox()
        self.check_box.setObjectName("checkBox")

        description_layout = QVBoxLayout()
        description_layout.setContentsMargins(0, 0, 0, 0)
        description_layout.setSpacing(1)

        header = QLabel(self.header_text)
        header.setObjectName("header")

        description = QLabel(self.description_text)
        description.setObjectName("description")
        description.setWordWrap(True)

        description_layout.addWidget(header)
        description_layout.addWidget(description)

        container_layout.addWidget(self.check_box)
        container_layout.addLayout(description_layout, 1)

        main_layout.addWidget(container_widget)

    def returnValue(self):
        return self.check_box.isChecked()

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container {{
                background-color: {COLOR_CARD_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
            }}
            QCheckBox#checkBox {{
                background: transparent;
            }}
            QCheckBox#checkBox::indicator {{
                width: 15px;
                height: 15px;

                background-color: {COLOR_CARD_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 2px;
            }}
            QCheckBox#checkBox::indicator:hover {{
                background-color: {COLOR_ACCENT_BLUE_BG};
                border: 1px solid {COLOR_ACCENT_BLUE};
            }}
            QCheckBox#checkBox::indicator:checked {{
                background-color: {COLOR_ACCENT_BLUE};
                border: 1px solid {COLOR_ACCENT_BLUE};
                image: url('resources/tick.svg');
            }}
            QCheckBox#checkBox::indicator:checked:hover {{
                background-color: {COLOR_ACCENT_BLUE};
                border: 1px solid {COLOR_ACCENT_BLUE};
            }}
            QLabel#header {{
                font-family: '{FONT_FAMILY}';
                font-size: 14px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background: transparent;
            }}
           QLabel#description {{
                font-family: '{FONT_FAMILY}';
                font-size: 13px;
                font-weight: 400;
                color: {COLOR_TEXT_MUTED};
                background: transparent;
            }}
        """)
