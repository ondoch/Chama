from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
)

from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
    COLOR_SIDEBAR_BG,
)

TICK_ICON_PATH = "resources/done_tick.svg"
TICK_SIZE = 22


class Timetable(QFrame):
    def __init__(self, name="", amount="", date="", completed=False):
        super().__init__()

        self.completed = completed

        self.setObjectName("card")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(90)

        self.initUi(name, amount, date)
        self.setStylesheet()

    def initUi(self, name, amount, date):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(14, 10, 14, 10)
        main_layout.setSpacing(8)

        details_layout = QVBoxLayout()
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(2)

        self.name = QLabel(name)
        self.name.setObjectName("name")

        self.amount = QLabel(amount)
        self.amount.setObjectName("amount")

        self.date = QLabel(date)
        self.date.setObjectName("date")

        details_layout.addWidget(self.name)
        details_layout.addWidget(self.amount)
        details_layout.addWidget(self.date)

        self.tick = QLabel()
        self.tick.setObjectName("tick")
        self.tick.setAlignment(Qt.AlignCenter)
        self.tick.setFixedSize(TICK_SIZE, TICK_SIZE)
        self.tick.setPixmap(
            QIcon(TICK_ICON_PATH).pixmap(QSize(TICK_SIZE, TICK_SIZE))
        )
        self.tick.setVisible(self.completed)

        main_layout.addLayout(details_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.tick, alignment=Qt.AlignVCenter)

    def set_completed(self, completed):
        self.completed = bool(completed)
        self.tick.setVisible(self.completed)
        self.setStylesheet()

    def setStylesheet(self):
        if self.completed:
            card_bg = COLOR_SIDEBAR_BG
            card_border = COLOR_SIDEBAR_BG
            name_color = "#FFFFFF"
            amount_color = "#FFFFFF"
            date_color = "#FFFFFF"
        else:
            card_bg = "transparent"
            card_border = COLOR_BORDER
            name_color = COLOR_TEXT_PRIMARY
            amount_color = COLOR_TEXT_PRIMARY
            date_color = COLOR_TEXT_MUTED

        self.setStyleSheet(f"""
            QFrame#card{{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 6px;
            }}
            QLabel#name{{
                font-family: {FONT_FAMILY};
                color: {name_color};
                font-size: 13px;
                font-weight: 600;
                background: transparent;
                border: none;
            }}
            QLabel#amount{{
                font-family: {FONT_FAMILY};
                color: {amount_color};
                font-size: 13px;
                background: transparent;
                border: none;
            }}
            QLabel#date{{
                font-family: {FONT_FAMILY};
                color: {date_color};
                font-size: 12px;
                background: transparent;
                border: none;
            }}
            QLabel#tick{{
                background: transparent;
                border: none;
            }}
        """)
