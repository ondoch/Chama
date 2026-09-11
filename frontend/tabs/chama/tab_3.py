from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import (
    Qt, 
    pyqtSignal,
    QSize
)
from PyQt5.QtGui import QIcon

from widgets.widget_9 import MembersTable
from widgets.widget_10 import Official
from widgets.widget_11 import SummaryWidget
from components.banner import Banner
from components.style_constants import (
    COLOR_CARD_BG, 
    COLOR_BORDER, 
    COLOR_ACCENT_BLUE
)


class Tab3(QFrame):
    cancel_clicked = pyqtSignal()
    finish_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container_widget = QWidget()
        container_widget.setFixedWidth(1100)
        container_widget.setObjectName("container")
        container_widget_layout = QVBoxLayout(container_widget)

        banner = Banner("resources/group_svg.svg", "Basic Information", "Provide fundamental details about the Chama")
        container_widget_layout.addWidget(banner, alignment=Qt.AlignLeft)

        row_container = QWidget()
        row_container_layout = QHBoxLayout(row_container)
        row_container_layout.setSpacing(15)

        row_1 = QVBoxLayout()
        row_2 = QVBoxLayout()
        row_3 = QVBoxLayout()

        members_table = MembersTable()
        officials = Official()
        summary = SummaryWidget()
        row_1.addWidget(members_table)
        row_2.addWidget(officials)
        row_3.addWidget(summary)
        row_3.addStretch()

        row_container_layout.addLayout(row_1)
        row_container_layout.addLayout(row_2)
        row_container_layout.addLayout(row_3)

        nav_row = QHBoxLayout()
        nav_row.setContentsMargins(10, 0, 10, 0)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(QIcon("resources/cancel.svg"))
        self.cancel_btn.setIconSize(QSize(16, 16))
        self.cancel_btn.setLayoutDirection(Qt.LeftToRight)
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.setStyleSheet(f"padding: 8px 16px; border:1px solid {COLOR_ACCENT_BLUE}; color: #000; border-radius: 6px")

        self.finish_btn = QPushButton("Finish")
        self.finish_btn.setIcon(QIcon("resources/tick.svg"))
        self.finish_btn.setIconSize(QSize(16, 16))
        self.finish_btn.setLayoutDirection(Qt.RightToLeft)
        self.finish_btn.setMinimumWidth(100)
        self.finish_btn.setStyleSheet(f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px")

        for btn in (self.cancel_btn, self.finish_btn):
            btn.setCursor(Qt.PointingHandCursor)

        self.cancel_btn.clicked.connect(self.cancel_clicked.emit)
        self.finish_btn.clicked.connect(self.finish_clicked.emit)

        nav_row.addWidget(self.cancel_btn)
        nav_row.addStretch()
        nav_row.addWidget(self.finish_btn)

        container_widget_layout.addWidget(row_container)
        container_widget_layout.addLayout(nav_row)

        main_layout.addStretch()
        main_layout.addWidget(container_widget, alignment=Qt.AlignHCenter)
        main_layout.addStretch()

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container{{
                background: {COLOR_CARD_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
            }}
        """)
