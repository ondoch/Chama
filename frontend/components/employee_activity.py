from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtGui import (
    QPixmap,
    QColor,
    QPainter,
    QPainterPath,
)
from PyQt5.QtCore import Qt

from components.style_constants import (
    COLOR_BORDER,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    FONT_FAMILY,
)

# local placeholder image used while you are still styling
DEFAULT_AVATAR = "resources/avatar.jpeg"


class EmployeeActivity(QFrame):
    """One row in the 'Recent Employee Activity' list."""

    def __init__(
        self,
        name="Joshua Mochama",
        activity="Created new chama 'Mwangaza Women Group'",
        time_text="2 hours ago",
        avatar_path=DEFAULT_AVATAR,
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("employee_activity")
        self.avatar_path = avatar_path

        self.initUi(name, activity, time_text)
        self.setStylesheet()

    def initUi(self, name, activity, time_text):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(12)

        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(36, 36)
        self.avatar_label.setPixmap(self.circularPixmap(self.avatar_path, 36))

        description_container = QWidget()
        description_container_layout = QVBoxLayout(description_container)
        description_container_layout.setContentsMargins(0, 0, 0, 0)
        description_container_layout.setSpacing(2)

        self.name_label = QLabel(name)
        self.name_label.setObjectName("name_label")

        self.activity_label = QLabel(activity)
        self.activity_label.setObjectName("activity_label")
        self.activity_label.setWordWrap(True)

        description_container_layout.addWidget(self.name_label)
        description_container_layout.addWidget(self.activity_label)

        self.time_label = QLabel(time_text)
        self.time_label.setObjectName("time_label")

        main_layout.addWidget(self.avatar_label)
        main_layout.addWidget(description_container, 1)   # takes the free width
        main_layout.addWidget(
            self.time_label, alignment=Qt.AlignRight | Qt.AlignTop
        )

    def circularPixmap(self, path, size):
        source = QPixmap(path)
        if source.isNull():
            # image missing -> plain coloured circle instead of crashing
            source = QPixmap(size, size)
            source.fill(QColor("#7C6EF8"))

        # fill the square, then crop from the centre so the image isn't offset
        source = source.scaled(
            size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        x = (source.width() - size) // 2
        y = (source.height() - size) // 2
        source = source.copy(x, y, size, size)

        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        clip = QPainterPath()
        clip.addEllipse(0, 0, size, size)
        painter.setClipPath(clip)
        painter.drawPixmap(0, 0, source)
        painter.end()

        return rounded

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QFrame#employee_activity{{
                border: none;
                border-bottom: 1px solid {COLOR_BORDER};
                background: transparent;
            }}
            QLabel#name_label{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_PRIMARY};
                font-size: 14px;
                font-weight: 600;
            }}
            QLabel#activity_label{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_MUTED};
                font-size: 13px;
            }}
            QLabel#time_label{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_MUTED};
                font-size: 12px;
            }}
        """)
