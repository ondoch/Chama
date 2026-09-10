from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

from components.style_constants import (
    COLOR_BORDER,
    FONT_FAMILY,
    COLOR_TEXT_MUTED
)

class ProgressWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        container = QWidget()
        container.setObjectName("overall_container")
        container_layout = QVBoxLayout(container)
        self.setFixedWidth(300)

        label_1 = QLabel("Uploading")
        label_1.setObjectName("label_1")

        layout_1 = QVBoxLayout()
        layout_2 = QHBoxLayout()
        layout_3 = QHBoxLayout()
        layout_4 = QVBoxLayout()

        file_name = QLabel("file_name.jpg")
        file_name.setObjectName("file_name")
        file_size = QLabel("10.5MB")
        file_size.setObjectName("file_size")

        layout_1.addWidget(file_name)
        layout_1.addWidget(file_size)
        layout_1.setSpacing(1)
        layout_1.setContentsMargins(0,0,0,0)

        icon = QLabel()
        icon.setFixedSize(32,32)
        pixmap = QPixmap("resources/file_upload.svg")
        icon.setPixmap(pixmap.scaled(32,32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        layout_2.addWidget(icon)
        layout_2.addLayout(layout_1)
        layout_2.setContentsMargins(0,0,0,0)

        cancel_btn = QPushButton()
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setIcon(QIcon("resources/cancel.svg"))

        layout_3.addLayout(layout_2)
        layout_3.addStretch()
        layout_3.addWidget(cancel_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)

        layout_4.addLayout(layout_3)
        layout_4.addWidget(self.progress_bar)

        container_layout.addLayout(layout_4)
        main_layout.addWidget(label_1)
        main_layout.addWidget(container)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#overall_container{{
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
            }}
            QProgressBar{{
                background-color: #e5e7eb;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: #1e3a8a;
                border-radius: 3px;
            }}
            QPushButton{{
                border: none;
            }}
            QLabel#label_1{{
                font-family:{FONT_FAMILY};
                font-size:11px;
            }}
            QLabel#file_name{{
                font-family:{FONT_FAMILY};
                font-size:12px;
            }}
            QLabel#file_size{{
                font-family:{FONT_FAMILY};
                font-size:11px;
                color: {COLOR_TEXT_MUTED}
            }}
        """)
