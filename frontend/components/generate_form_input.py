from PyQt5.QtWidgets import(
    QFrame,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QLabel)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

class GenerateFormInput(QFrame):
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

        label = QLabel(self.placeholder)
        label.setObjectName("label")

        generate_btn = QPushButton()
        generate_btn.setObjectName("generate_btn")
        generate_btn.setIcon(QIcon("resources/generate.svg"))
        generate_btn.setIconSize(QSize(18,18))
        generate_btn.setCursor(Qt.PointingHandCursor)

        frame_layout.addWidget(icon)
        frame_layout.addWidget(separator)
        frame_layout.addWidget(label)
        frame_layout.addStretch()
        frame_layout.addWidget(generate_btn)
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
            QLabel#label{
                border: none;
                background: transparent;
                font-size: 12px;
                font-family: Arial, sans-serif;
            }
            QPushButton#generate_btn{
                border: none;
                background: transparent;
                margin-right: 10px;
            }
        """)
