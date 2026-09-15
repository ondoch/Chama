import os
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon

from components.style_constants import (
    COLOR_BORDER,
    FONT_FAMILY,
    COLOR_TEXT_MUTED
)


class ProgressWidget(QWidget):
    upload_finished = pyqtSignal(str)
    upload_cancelled = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._current_file = None
        self.hide()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container.setObjectName("overall_container")
        container_layout = QVBoxLayout(container)
        self.setFixedWidth(300)

        label_1 = QLabel("Uploading")
        label_1.setObjectName("label_1")

        layout_1 = QVBoxLayout()
        layout_2 = QHBoxLayout()
        layout_3 = QHBoxLayout()
        layout_4 = QVBoxLayout()

        self.file_name_label = QLabel("file_name.jpg")
        self.file_name_label.setObjectName("file_name")
        self.file_size_label = QLabel("0 MB")
        self.file_size_label.setObjectName("file_size")

        layout_1.addWidget(self.file_name_label)
        layout_1.addWidget(self.file_size_label)
        layout_1.setSpacing(1)
        layout_1.setContentsMargins(0, 0, 0, 0)

        icon = QLabel()
        icon.setFixedSize(32, 32)
        pixmap = QPixmap("resources/file_upload.svg")
        icon.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        layout_2.addWidget(icon)
        layout_2.addLayout(layout_1)
        layout_2.setContentsMargins(0, 0, 0, 0)

        self.cancel_btn = QPushButton()
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setIcon(QIcon("resources/cancel.svg"))
        self.cancel_btn.clicked.connect(self.cancel_upload)

        layout_3.addLayout(layout_2)
        layout_3.addStretch()
        layout_3.addWidget(self.cancel_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)

        layout_4.addLayout(layout_3)
        layout_4.addWidget(self.progress_bar)

        container_layout.addLayout(layout_4)
        main_layout.addWidget(label_1)
        main_layout.addWidget(container)

    def start_upload(self, file_path):
        """Show the widget and begin (simulated) progress for file_path."""
        self._current_file = file_path
        self.file_name_label.setText(os.path.basename(file_path))
        try:
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            self.file_size_label.setText(f"{size_mb:.1f} MB")
        except OSError:
            self.file_size_label.setText("")

        self.progress_bar.setValue(0)
        self.show()
        self._timer.start(80)

    def _tick(self):
        value = self.progress_bar.value() + 4
        if value >= 100:
            self.progress_bar.setValue(100)
            self._timer.stop()
            self.upload_finished.emit(self._current_file)
        else:
            self.progress_bar.setValue(value)

    def cancel_upload(self):
        self._timer.stop()
        self.progress_bar.setValue(0)
        self.hide()
        self.upload_cancelled.emit()

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#overall_container{{
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
            }}
            QProgressBar{{
                background-color: #e5e7eb;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: #1e3a8a;
                border-radius: 3px;
            }}
            QPushButton{{
                border: none;
            }}
            QLabel#label_1{{
                font-family:{FONT_FAMILY};
                font-size:11px;
            }}
            QLabel#file_name{{
                font-family:{FONT_FAMILY};
                font-size:12px;
            }}
            QLabel#file_size{{
                font-family:{FONT_FAMILY};
                font-size:11px;
                color: {COLOR_TEXT_MUTED}
            }}
        """)