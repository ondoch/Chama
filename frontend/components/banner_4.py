from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from components.style_constants import (
    COLOR_BORDER,
    FONT_FAMILY,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED
)

class Banner4(QWidget):
    def __init__(self, icon_path, header, sub_header_1, sub_header_2=None):
        super().__init__()
        self.icon_path = icon_path
        self.header = header
        self.sub_header_1 = sub_header_1
        self.sub_header_2 = sub_header_2
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 0, 6, 0)

        container_widget = QWidget()
        container_widget.setObjectName("container")
        container_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        container_widget.setMinimumWidth(160)
        container_widget.setMinimumHeight(100)

        container_widget_layout = QHBoxLayout(container_widget)
        container_widget_layout.setContentsMargins(16, 14, 16, 14)
        container_widget_layout.setSpacing(12)

        icon_wrapper = QWidget()
        icon_wrapper.setObjectName("icon_wrapper")
        icon_wrapper.setFixedSize(52, 52)
        icon_wrapper_layout = QHBoxLayout(icon_wrapper)
        icon_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        icon_wrapper_layout.setAlignment(Qt.AlignCenter)

        icon = QLabel()
        icon.setFixedSize(40, 40)
        pixmap = QPixmap(self.icon_path)
        icon.setPixmap(pixmap.scaled(39, 39, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_wrapper_layout.addWidget(icon)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        header = QLabel(self.header)
        header.setObjectName("header")
        sub_header_1 = QLabel(self.sub_header_1)
        sub_header_1.setObjectName("sub_header_1")

        info_layout.addWidget(header, alignment=Qt.AlignLeft)
        info_layout.addWidget(sub_header_1, alignment=Qt.AlignLeft)

        if self.sub_header_2:
            sub_header_2 = QLabel(self.sub_header_2)
            sub_header_2.setObjectName("sub_header_2")
            info_layout.addWidget(sub_header_2, alignment=Qt.AlignLeft)

        container_widget_layout.addWidget(icon_wrapper, alignment=Qt.AlignVCenter)
        container_widget_layout.addLayout(info_layout)
        container_widget_layout.setAlignment(info_layout, Qt.AlignVCenter)
        container_widget_layout.addStretch()

        main_layout.addWidget(container_widget)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container{{
                border: 1px solid {COLOR_BORDER};
                background-color: #FFFFFF;
                border-radius: 10px;
            }}
            QWidget#icon_wrapper{{
                background-color: #EEF3FF;
                border-radius: 26px;
            }}
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 700;
            }}
            QLabel#sub_header_1{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 13px;
                font-weight: 500;
            }}
            QLabel#sub_header_2{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 11px;
            }}
        """)
