from PyQt5.QtWidgets import(
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Banner(QFrame):
    def __init__(self, icon_path, title, sub_title):
        super().__init__()

        self.icon_path = icon_path
        self.title = title
        self.sub_title = title

        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        header_layout = QHBoxLayout()
        header_label_layout = QVBoxLayout()
        header_label_layout.setContentsMargins(0,0,0,0)

        icon = QLabel()
        pixmap = QPixmap(self.icon_path)
        icon.setPixmap(pixmap.scaled(47, 47, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        title = QLabel(self.title)
        title.setObjectName("title")
        sub_title = QLabel(self.sub_title)
        sub_title.setObjectName("sub_title")

        header_label_layout.addWidget(title)
        header_label_layout.addWidget(sub_title)

        header_layout.addWidget(icon)
        header_layout.addLayout(header_label_layout)

        main_layout.addLayout(header_layout)
        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet("""
            QLabel#title{
                font-family: "Segoe UI";
                font-size: 20px;
                font-weight: 600;
                color: #1F2937;
            }
            QLabel#sub_title {
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 400;
                color: #6B7280;
            }
        """)
