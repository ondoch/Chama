from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class MenuBtn(QPushButton):
    def __init__(self, text="", icon_path=None, parent=None):
        super().__init__(text, parent)
        self.icon_path = icon_path
        self.initUI()

    def initUI(self):
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)

        if self.icon_path:
            self.setIcon(QIcon(self.icon_path))
            self.setIconSize(QSize(20, 20))

        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px 16px;
                border: none;
                border-left: 3px solid transparent;
                background: transparent;
                color: #333333;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #F0F0F0;
            }
            QPushButton:checked {
                border-left: 3px solid #4A90D9;
                background: #E8F0FB;
                color: #4A90D9;
                font-weight: bold;
            }
            QPushButton:pressed {
                background: #DCE8F7;
            }
        """)
