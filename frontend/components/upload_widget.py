from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from components.style_constants import (
    COLOR_BORDER,
    COLOR_TEXT_MUTED
)


class UploadWidget(QFrame):
    file_selected = pyqtSignal(str)

    def __init__(self, header):
        super().__init__()
        self.header = header
        self.initUI()
        self.setStylesheet()
        self.setAcceptDrops(True)

    def initUI(self):
        main_layout = QHBoxLayout(self)

        container_widget = QWidget()
        container_widget_layout = QVBoxLayout(container_widget)

        self.drop_widget = QWidget()
        self.drop_widget.setFixedHeight(140)
        self.drop_widget.setFixedWidth(300)
        self.drop_widget.setObjectName("drop_widget")
        drop_widget_layout = QVBoxLayout(self.drop_widget)

        label = QLabel(self.header)
        label.setObjectName("title")
        container_widget_layout.addWidget(label, alignment=Qt.AlignCenter)

        icon = QLabel()
        icon.setFixedSize(50, 50)
        pixmap = QPixmap("resources/upload.svg")
        icon.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.setAlignment(Qt.AlignCenter)

        self.hint_label = QLabel()
        self.hint_label.setAlignment(Qt.AlignHCenter)
        self.hint_label.setTextFormat(Qt.RichText)
        self.hint_label.setText(self.hint_html())
        self.hint_label.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 13px;")
        self.hint_label.setOpenExternalLinks(False)
        self.hint_label.linkActivated.connect(self.open_file_dialog)

        drop_widget_layout.addStretch()
        drop_widget_layout.addWidget(icon, alignment=Qt.AlignCenter)
        drop_widget_layout.addWidget(self.hint_label, alignment=Qt.AlignCenter)
        drop_widget_layout.addStretch()

        container_widget_layout.addWidget(self.drop_widget, alignment=Qt.AlignCenter)

        main_layout.addWidget(container_widget)

    @staticmethod
    def hint_html():
        return (
            'Drag and drop your file here or '
            '<a href="#choose" style="color:#1e3a8a; font-weight:600; '
            'text-decoration:none;">choose image</a>'
        )

    def open_file_dialog(self, _link=None):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file",
            "",
            "Images (*.png *.jpg *.jpeg);;PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            self.file_selected.emit(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path:
                self.file_selected.emit(file_path)
        event.acceptProposedAction()

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
