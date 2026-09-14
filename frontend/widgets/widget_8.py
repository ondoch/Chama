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

        self.upload_widget = UploadWidget(self.header)
        self.progress_widget = ProgressWidget()

        main_layout.addWidget(self.upload_widget, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.progress_widget, alignment=Qt.AlignHCenter)

        self.upload_widget.file_selected.connect(self.handle_file_selected)
        self.progress_widget.upload_finished.connect(self.handle_upload_finished)
        self.progress_widget.upload_cancelled.connect(self.handle_upload_cancelled)

    def handle_file_selected(self, file_path):
        self.upload_widget.hide()
        self.progress_widget.start_upload(file_path)

    def handle_upload_finished(self, file_path):
        self.upload_widget.show()

    def handle_upload_cancelled(self):
        self.upload_widget.show()
