from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from components.footer_btn import FooterButton
from components.style_constants import FONT_FAMILY


class Pagination(QWidget):
    page_changed = pyqtSignal(int)

    def __init__(self, page_size=10, noun="logs"):
        super().__init__()
        self.page_size = page_size
        self.noun = noun
        self.initUI()
        self.setStylesheet()
        self.set_state(1, 0)

    def initUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel()
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.page_nav = FooterButton()
        self.page_nav.page_changed.connect(self.page_changed.emit)

        main_layout.addWidget(self.label, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        main_layout.addStretch()
        main_layout.addWidget(self.page_nav, alignment=Qt.AlignVCenter | Qt.AlignRight)

    def set_state(self, page, total, page_size=None):
        """page = current page (1-based), total = total number of records."""
        if page_size:
            self.page_size = page_size

        total_pages = max(1, -(-total // self.page_size))
        if total == 0:
            self.label.setText(f"No {self.noun} found")
        else:
            start = (page - 1) * self.page_size + 1
            end = min(page * self.page_size, total)
            self.label.setText(f"Showing {start} to {end} of {total} {self.noun}")
        self.page_nav.set_state(page, total_pages)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#label{{
                font-family: {FONT_FAMILY};
                font-size: 14px;
            }}
        """)
