from PyQt5.QtWidgets import (
    QDialog,
    QFrame,
    QWidget,
    QLabel,
    QTabWidget,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from components.status_badge import StatusBadge
from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
    COLOR_SIDEBAR_BG,
)

from widgets.overview import Overview
# from widgets.contributions import Contributions
# from widgets.loans import Loans
# from widgets.members import Members
# from widgets.cycle import Cycle
# from widgets.transactions import Transactions

COLOR_ACCENT = "#0F9D6B"

class PlaceholderPage(QWidget):

    def __init__(self, name):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel(f"{name} page coming soon")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            f"font-family: {FONT_FAMILY}; color: {COLOR_TEXT_MUTED}; font-size: 14px;"
        )
        layout.addWidget(label)


class ReportModal(QDialog):
    def __init__(self, row_data=None, parent=None):
        super().__init__(parent)
        self.setModal(True)

        self.initUi()
        self.setStylesheet()

        if row_data:
            self.set_data(row_data)

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container_widget = QWidget()
        container_widget.setObjectName("container_widget")
        container_widget_layout = QVBoxLayout(container_widget)

        container_widget_layout.addWidget(self.build_header())
        container_widget_layout.addWidget(self.build_tabs(), stretch=1)

        main_layout.addWidget(container_widget)

    def build_header(self):
        header_widget = QWidget()
        header_widget_layout = QHBoxLayout(header_widget)
        header_widget_layout.setContentsMargins(20, 0, 0, 0)
        header_widget_layout.setSpacing(0)

        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(10, 0, 0, 0)

        icon = QLabel()
        icon.setFixedSize(50, 50)
        pixmap = QPixmap("resources/group_1.svg")
        icon.setPixmap(
            pixmap.scaled(49, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        self.header = QLabel("Umoja Self-help group")
        self.header.setObjectName("header")

        container_1 = QWidget()
        container_1_layout = QHBoxLayout(container_1)
        container_1_layout.setContentsMargins(0, 5, 0, 0)
        container_1_layout.setSpacing(12)

        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(6)

        layout_2 = QHBoxLayout()
        layout_2.setContentsMargins(0, 0, 0, 0)
        layout_2.setSpacing(6)

        label_1 = QLabel("Cycle:")
        label_1.setObjectName("label")

        self.cycle = QLabel("Jan 2025 - Dec 2025")
        self.cycle.setObjectName("label")

        layout_1.addWidget(label_1)
        layout_1.addWidget(self.cycle)

        label_2 = QLabel("Status:")
        label_2.setObjectName("label")

        self.status = StatusBadge("Active")

        layout_2.addWidget(label_2)
        layout_2.addWidget(self.status)

        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Plain)
        divider.setObjectName("divider")
        divider.setFixedWidth(1)
        divider.setFixedHeight(20)

        container_1_layout.addLayout(layout_1)
        container_1_layout.addWidget(divider, alignment=Qt.AlignVCenter)
        container_1_layout.addLayout(layout_2)
        container_1_layout.addStretch()

        container_1_layout.setAlignment(layout_1, Qt.AlignVCenter)
        container_1_layout.setAlignment(layout_2, Qt.AlignVCenter)

        header_layout.addWidget(self.header)
        header_layout.addWidget(container_1)

        header_widget_layout.addWidget(icon, alignment=Qt.AlignTop)
        header_widget_layout.addLayout(header_layout)
        header_widget_layout.addStretch()

        return header_widget

    def build_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setObjectName("report_tabs")
        self.tabs.setDocumentMode(True)
        self.tabs.tabBar().setExpanding(False)
        self.tabs.tabBar().setDrawBase(False)
        self.tabs.tabBar().setCursor(Qt.PointingHandCursor)

        self.overview = Overview()
        pages = [
            ("Overview", self.overview),
            ("Contributions", PlaceholderPage("Contributions")),
            ("Loans", PlaceholderPage("Loans")),
            ("Members", PlaceholderPage("Members")),
            ("Cycle", PlaceholderPage("Cycle")),
            ("Transactions", PlaceholderPage("Transactions")),
        ]

        self.pages = {}
        for title, page in pages:
            self.tabs.addTab(page, title)
            self.pages[title] = page

        return self.tabs

    def set_data(self, row_data):
        self.header.setText(row_data.get("chama_name", "Report"))
        for page in self.pages.values():
            if hasattr(page, "set_data"):
                page.set_data(row_data)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container_widget{{
                border: 1px solid {COLOR_BORDER};
                background-color: #FFFFFF;
                border-radius: 10px;
            }}
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 600;
            }}
            QLabel#label{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_MUTED};
                font-size: 14px;
            }}
            QFrame#divider{{
                background-color: {COLOR_BORDER};
                border: none;
            }}

            QTabWidget#report_tabs::pane{{
                border: none;
                border-top: 1px solid {COLOR_BORDER};
                background: transparent;
            }}
            QTabWidget#report_tabs QTabBar{{
                background: transparent;
            }}
            QTabWidget#report_tabs QTabBar::tab{{
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {COLOR_TEXT_MUTED};
                background: transparent;
                border: none;
                border-bottom: 2px solid transparent;
                padding: 10px 18px;
                margin-right: 6px;
            }}
            QTabWidget#report_tabs QTabBar::tab:hover{{
                color: {COLOR_TEXT_PRIMARY};
            }}
            QTabWidget#report_tabs QTabBar::tab:selected{{
                color: {COLOR_SIDEBAR_BG};
                font-weight: 600;
                border-bottom: 2px solid {COLOR_SIDEBAR_BG};
            }}
        """)
