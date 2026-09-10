from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from components.style_constants import (
    COLOR_BORDER,
    COLOR_TEXT_MUTED
)

class UploadWidget(QFrame):
    def __init__(self, header):
        super().__init__()
        self.header = header
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        container_widget = QWidget()
        container_widget_layout = QVBoxLayout(container_widget)

        drop_widget = QWidget()
        drop_widget.setFixedHeight(140)
        drop_widget.setFixedWidth(300)
        drop_widget.setObjectName("drop_widget")
        drop_widget_layout = QVBoxLayout(drop_widget)

        label = QLabel(self.header)
        label.setObjectName("title")
        container_widget_layout.addWidget(label, alignment=Qt.AlignCenter)

        icon = QLabel()
        icon.setFixedSize(50,50)
        pixmap = QPixmap("resources/upload.svg")
        icon.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.setAlignment(Qt.AlignCenter)

        self.hint_label = QLabel()
        self.hint_label.setAlignment(Qt.AlignHCenter)
        self.hint_label.setTextFormat(Qt.RichText)
        self.hint_label.setText(self.hint_html())
        self.hint_label.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 13px;")

        drop_widget_layout.addStretch()
        drop_widget_layout.addWidget(icon, alignment = Qt.AlignCenter)
        drop_widget_layout.addWidget(self.hint_label, alignment = Qt.AlignCenter)
        drop_widget_layout.addStretch()

        container_widget_layout.addWidget(drop_widget, alignment=Qt.AlignCenter)

        main_layout.addWidget(container_widget)

    @staticmethod
    def hint_html():
        return (
            'Drag and drop your file here or '
            '<a href="#choose" style="color:#1e3a8a; font-weight:600; '
            'text-decoration:none;">choose image</a>'
        )

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#drop_widget{{
                border: 2px dashed {COLOR_BORDER};
                border-radius: 10px;
            }}
            QLabel#title{{
                font-family: "Segoe UI";
                font-size: 16px;
                font-weight: 600;
                color: {COLOR_TEXT_MUTED};
            }}
        """)
