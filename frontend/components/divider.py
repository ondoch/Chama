from PyQt5.QtWidgets import QFrame

class Divider(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setStyleSheet("color:#E4E6EC;")
