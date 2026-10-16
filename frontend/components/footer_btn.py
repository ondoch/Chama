from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, pyqtSignal


class FooterButton(QWidget):
    """Prev / numbered pages / Next. Emits page_changed(int)."""

    page_changed = pyqtSignal(int)
    MAX_VISIBLE = 5

    def __init__(self):
        super().__init__()
        self.page = 1
        self.total_pages = 1
        self.initUI()
        self.setStylesheet()
        self.set_state(1, 1)

    def initUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.previous_btn = QPushButton()
        self.previous_btn.setIcon(QIcon("resources/arrow-left.svg"))
        self.previous_btn.setIconSize(QSize(15, 15))
        self.previous_btn.setFixedSize(30, 30)
        self.previous_btn.clicked.connect(lambda: self.page_changed.emit(self.page - 1))

        self.next_btn = QPushButton()
        self.next_btn.setIcon(QIcon("resources/arrow-right.svg"))
        self.next_btn.setIconSize(QSize(15, 15))
        self.next_btn.setFixedSize(30, 30)
        self.next_btn.clicked.connect(lambda: self.page_changed.emit(self.page + 1))

        self.pages_layout = QHBoxLayout()
        self.pages_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.previous_btn)
        main_layout.addLayout(self.pages_layout)
        main_layout.addWidget(self.next_btn)

    def set_state(self, page, total_pages):
        """Rebuild the numbered buttons for the given page / page count."""
        self.page = page
        self.total_pages = max(1, total_pages)

        while self.pages_layout.count():
            item = self.pages_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        end = min(self.total_pages, max(1, page - self.MAX_VISIBLE // 2) + self.MAX_VISIBLE - 1)
        start = max(1, end - self.MAX_VISIBLE + 1)

        for n in range(start, end + 1):
            btn = QPushButton(str(n))
            btn.setFixedSize(30, 30)
            btn.setProperty("current", n == page)
            btn.clicked.connect(lambda _checked, n=n: self._on_page_clicked(n))
            self.pages_layout.addWidget(btn)

        self.previous_btn.setEnabled(page > 1)
        self.next_btn.setEnabled(page < self.total_pages)

    def _on_page_clicked(self, n):
        if n != self.page:
            self.page_changed.emit(n)

    def setStylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                border: 1px solid #ccc;
                background-color: #f5f5f5;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:disabled {
                background-color: #fafafa;
                color: #aaa;
            }
            QPushButton[current="true"] {
                background-color: #4a90e2;
                color: white;
                border: 1px solid #357abd;
            }
        """)
