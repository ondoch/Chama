from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout
)
from PyQt5.QtCore import Qt
from components.upload_widget import UploadWidget
from components.progress_widget import ProgressWidget

class UploadContainer(QFrame):
    def __init__(self, header):
        super().__init__()
        self.header = header
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        upload_1 = UploadWidget(self.header)
        progress_1 = ProgressWidget()
        main_layout.addWidget(upload_1, alignment=Qt.AlignHCenter)
        main_layout.addWidget(progress_1, alignment=Qt.AlignHCenter)
