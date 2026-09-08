import os
from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QPushButton,
    QFileDialog, 
    QListWidget, 
    QListWidgetItem, 
    QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal


class FileUploadWidget(QWidget):
    filesSelected = pyqtSignal(list)

    def __init__(self, parent=None, allow_multiple=True, file_filter="All Files (*)"):
        super().__init__(parent)
        self.allow_multiple = allow_multiple
        self.file_filter = file_filter
        self._file_paths = []

        self.setAcceptDrops(True)
        self.buildUI()

    def buildUI(self):
        layout = QVBoxLayout(self)

        self.drop_zone = QFrame()
        self.drop_zone.setObjectName("dropZone")
        self.drop_zone.setFrameShape(QFrame.StyledPanel)
        self.drop_zone.setMinimumHeight(100)
        self.drop_zone.setStyleSheet("""
            QFrame#dropZone {
                border: 2px dashed #aaaaaa;
                border-radius: 8px;
                background-color: #fafafa;
            }
        """)

        drop_layout = QVBoxLayout(self.drop_zone)
        self.drop_label = QLabel("Drag & drop files here, or click Browse below")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("color: #888888; border: none;")
        drop_layout.addWidget(self.drop_label)

        browse_row = QHBoxLayout()
        self.browse_button = QPushButton("Browse Files")
        self.browse_button.clicked.connect(self.open_file_dialog)
        browse_row.addStretch()
        browse_row.addWidget(self.browse_button)
        browse_row.addStretch()

        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(120)

        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_files)

        layout.addWidget(self.drop_zone)
        layout.addLayout(browse_row)
        layout.addWidget(self.file_list)
        layout.addWidget(self.clear_button)

    def open_file_dialog(self):
        if self.allow_multiple:
            paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", self.file_filter)
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Select File", "", self.file_filter)
            paths = [path] if path else []

        if paths:
            self._add_files(paths)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_zone.setStyleSheet("""
                QFrame#dropZone {
                    border: 2px dashed #4CAF50;
                    border-radius: 8px;
                    background-color: #eef8ee;
                }
            """)

    def dragLeaveEvent(self, event):
        self.drop_zone.setStyleSheet("""
            QFrame#dropZone {
                border: 2px dashed #aaaaaa;
                border-radius: 8px;
                background-color: #fafafa;
            }
        """)

    def dropEvent(self, event):
        paths = [url.toLocalFile() for url in event.mimeData().urls() if url.isLocalFile()]
        self.dragLeaveEvent(event)
        if paths:
            if not self.allow_multiple:
                paths = paths[:1]
            self._add_files(paths)

    def _add_files(self, paths):
        if not self.allow_multiple:
            self._file_paths = []
            self.file_list.clear()

        for path in paths:
            if path and path not in self._file_paths:
                self._file_paths.append(path)
                item = QListWidgetItem(os.path.basename(path))
                item.setToolTip(path)
                self.file_list.addItem(item)

        self.filesSelected.emit(self._file_paths)

    def clear_files(self):
        self._file_paths = []
        self.file_list.clear()
        self.filesSelected.emit(self._file_paths)

    def get_selected_files(self):
        return self._file_paths
