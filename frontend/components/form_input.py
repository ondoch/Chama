from PyQt5.QtWidgets import(
    QFrame,
    QLineEdit,
    QHBoxLayout,
    QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class FormInput(QFrame):
    def __init__(self, icon_path, placeholder):
        super().__init__()
        self.icon_path = icon_path
        self.placeholder = placeholder
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout = QHBoxLayout ()
        frame_layout.setContentsMargins(0, 0, 0, 0)

        icon = QLabel("Icon")
        icon.setObjectName("icon")
        if self.icon_path:
            pixmap = QPixmap(self.icon_path)
            icon.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFixedWidth(1)
        separator.setFrameShape(QFrame.VLine)

        entry = QLineEdit()
        entry.setObjectName("entry")
        entry.setPlaceholderText(self.placeholder)

        frame_layout.addWidget(icon)
        frame_layout.addWidget(separator)
        frame_layout.addWidget(entry)
        main_layout.addLayout(frame_layout)

        self.setLayout(main_layout)
        self.setFixedHeight(40)

    def setStylesheet(self):
        self.setStyleSheet("""
            QFrame{
                border: 1px solid #D8DBDE;
                border-radius: 5px;
            }
            QLabel#icon{
                border: none;
                margin: 5px;
            }
            QFrame#separator{
                border: none;
                background-color: #D8DBDE;
            }
            QLineEdit#entry{
                border: none;
                background: transparent;
                font-size: 12px;
                font-family: Arial, sans-serif;
            }
        """)
