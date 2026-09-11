from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from components.style_constants import (
    COLOR_BORDER,
    FONT_FAMILY,
    COLOR_TEXT_PRIMARY,
    COLOR_ACCENT_BLUE,
    COLOR_ACCENT_BLUE_BG
)


class SummaryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        self.setFixedWidth(300)
        self.setMinimumHeight(220)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignCenter)

        widget_1 = QWidget()
        widget_1.setObjectName("widget_1")
        widget_1.setAttribute(Qt.WA_StyledBackground, True)

        widget_1_layout = QVBoxLayout(widget_1)
        widget_1_layout.setContentsMargins(16, 14, 16, 14)
        widget_1_layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        icon = QLabel()
        icon.setFixedSize(35, 35)
        pixmap = QPixmap("resources/sammury.svg")
        icon.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        header_label = QLabel("Assignment summary")
        header_label.setObjectName("header_label")

        header_layout.addWidget(icon)
        header_layout.addWidget(header_label)
        header_layout.addStretch()

        container_layout_1 = QGridLayout()
        container_layout_1.setHorizontalSpacing(2)
        container_layout_1.setVerticalSpacing(6)
        container_layout_1.setColumnStretch(0, 1)
        container_layout_1.setColumnStretch(1, 1)

        chama_label = QLabel("Chama:")
        chama_label.setObjectName("chama_label")
        members_selected = QLabel("Members Selected:")
        members_selected.setObjectName("members_selected")
        officials = QLabel("Officials:")
        officials.setObjectName("officials")

        chama_label_1 = QLabel("Mwangaza Women Group")
        chama_label_1.setObjectName("chama_label_1")
        chama_label_1.setWordWrap(True)
        members_selected_1 = QLabel("3")
        members_selected_1.setAlignment(Qt.AlignCenter)
        members_selected_1.setObjectName("members_selected_1")
        officials_1 = QLabel("3")
        officials_1.setAlignment(Qt.AlignCenter)
        officials_1.setObjectName("officials_1")

        container_layout_1.addWidget(chama_label, 0, 0)
        container_layout_1.addWidget(members_selected, 1, 0)
        container_layout_1.addWidget(officials, 2, 0)

        container_layout_1.addWidget(chama_label_1, 0, 1)
        container_layout_1.addWidget(members_selected_1, 1, 1)
        container_layout_1.addWidget(officials_1, 2, 1)

        widget_1_layout.addLayout(header_layout)
        widget_1_layout.addLayout(container_layout_1)

        widget_2 = QWidget()
        widget_2.setObjectName("widget_2")
        widget_2.setAttribute(Qt.WA_StyledBackground, True)

        widget_2_layout = QVBoxLayout(widget_2)
        widget_2_layout.setContentsMargins(16, 12, 16, 14)
        widget_2_layout.setSpacing(10)

        header_layout_2 = QHBoxLayout()
        header_layout_2.setSpacing(8)

        header_label_2 = QLabel("Selected Officials")
        header_label_2.setObjectName("header_label_2")
        header_layout_2.addWidget(header_label_2)
        header_layout_2.addStretch()

        container_layout_2 = QGridLayout()
        container_layout_2.setHorizontalSpacing(2)
        container_layout_2.setVerticalSpacing(6)
        container_layout_2.setColumnStretch(0, 1)
        container_layout_2.setColumnStretch(1, 1)

        chairperson_label = QLabel("John Kamau")
        chairperson_label.setObjectName("chairperson_label")
        chairperson_label.setAlignment(Qt.AlignCenter)
        secretary_label = QLabel("Jane Njeri")
        secretary_label.setObjectName("secretary_label")
        secretary_label.setAlignment(Qt.AlignCenter)
        treasurer_label = QLabel("Peter Otieno")
        treasurer_label.setObjectName("treasurer_label")
        treasurer_label.setAlignment(Qt.AlignCenter)

        chairperson_label_1 = QLabel("Chairperson")
        chairperson_label_1.setObjectName("chairperson_label_1")
        chairperson_label_1.setAlignment(Qt.AlignCenter)
        secretary_label_1 = QLabel("Secretary")
        secretary_label_1.setObjectName("secretary_label_1")
        secretary_label_1.setAlignment(Qt.AlignCenter)
        treasurer_label_1 = QLabel("Treasurer")
        treasurer_label_1.setObjectName("treasurer_label_1")
        treasurer_label_1.setAlignment(Qt.AlignCenter)

        container_layout_2.addWidget(chairperson_label, 0, 0)
        container_layout_2.addWidget(secretary_label, 1, 0)
        container_layout_2.addWidget(treasurer_label, 2, 0)

        container_layout_2.addWidget(chairperson_label_1, 0, 1)
        container_layout_2.addWidget(secretary_label_1, 1, 1)
        container_layout_2.addWidget(treasurer_label_1, 2, 1)

        widget_2_layout.addLayout(header_layout_2)
        widget_2_layout.addLayout(container_layout_2)

        main_layout.addWidget(widget_1)
        main_layout.addWidget(widget_2)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#widget_1{{
                background-color: {COLOR_ACCENT_BLUE_BG};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }}
            QWidget#widget_2{{
                border-left: 1px solid {COLOR_BORDER};
                border-right: 1px solid {COLOR_BORDER};
                border-bottom: 1px solid {COLOR_BORDER};
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }}
            QLabel#header_label{{
                font-family: '{FONT_FAMILY}';
                font-size: 16px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#header_label_2{{
                font-family: '{FONT_FAMILY}';
                font-size: 16px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#chama_label{{
                font-family: '{FONT_FAMILY}';
                font-size: 12px;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#members_selected{{
                font-family: '{FONT_FAMILY}';
                font-size: 12px;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#officials{{
                font-family: '{FONT_FAMILY}';
                font-size: 12px;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#chama_label_1{{
                font-family: '{FONT_FAMILY}';
                font-size: 11px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#members_selected_1{{
                font-family: '{FONT_FAMILY}';
                font-size: 11px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#officials_1{{
                font-family: '{FONT_FAMILY}';
                font-size: 11px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#chairperson_label{{
                font-family: '{FONT_FAMILY}';
                font-size: 12px;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#secretary_label{{
                font-family: '{FONT_FAMILY}';
                font-size: 12px;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#treasurer_label{{
                font-family: '{FONT_FAMILY}';
                font-size: 12px;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#chairperson_label_1{{
                font-family: '{FONT_FAMILY}';
                font-size: 11px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#secretary_label_1{{
                font-family: '{FONT_FAMILY}';
                font-size: 11px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#treasurer_label_1{{
                font-family: '{FONT_FAMILY}';
                font-size: 11px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
        """)
