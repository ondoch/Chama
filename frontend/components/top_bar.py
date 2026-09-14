from PyQt5.QtWidgets import (QFrame,
                             QWidget,
                             QHBoxLayout,
                             QVBoxLayout,
                             QPushButton,
                             QGraphicsDropShadowEffect,
                             QLabel,
                             QGridLayout)
from PyQt5.QtGui import (QFont,
                         QIcon,
                         QColor,
                         QPixmap,
                         QPainter,
                         QPainterPath)
from PyQt5.QtCore import Qt, QSize


class TopBar(QFrame):
    def __init__(self, user_name="Joshua Mochama", user_role="Administrator",
                 avatar_path="resources/avatar.jpeg", notification_count=3):
        super().__init__()

        self.user_name = user_name
        self.user_role = user_role
        self.avatar_path = avatar_path
        self.notification_count = notification_count

        self.setObjectName("top_bar")
        self.setFixedHeight(60)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 0, 15, 0)

        main_layout.addStretch()

        container_widget = QWidget()
        container_widget_layout = QHBoxLayout(container_widget)
        container_widget_layout.setContentsMargins(0, 0, 0, 0)
        container_widget_layout.setSpacing(15)

        bell_container = QWidget()
        bell_container.setFixedSize(36, 36)
        bell_grid = QGridLayout(bell_container)
        bell_grid.setContentsMargins(0, 0, 0, 0)

        self.bell_button = QPushButton()
        self.bell_button.setObjectName("bell_button")
        self.bell_button.setIcon(QIcon("resources/bell.svg"))
        self.bell_button.setIconSize(QSize(18, 18))
        self.bell_button.setFixedSize(36, 36)
        self.bell_button.setCursor(Qt.PointingHandCursor)

        self.badge = QLabel(str(self.notification_count))
        self.badge.setObjectName("badge")
        self.badge.setFixedSize(16, 16)
        self.badge.setAlignment(Qt.AlignCenter)
        self.badge.setVisible(self.notification_count > 0)

        bell_grid.addWidget(self.bell_button, 0, 0)
        bell_grid.addWidget(self.badge, 0, 0, alignment=Qt.AlignTop | Qt.AlignRight)

        profile_widget = QWidget()
        profile_widget.setObjectName("profile_widget")
        profile_layout = QHBoxLayout(profile_widget)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(10)
        profile_widget.setCursor(Qt.PointingHandCursor)

        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(36, 36)
        self.avatar_label.setPixmap(self.circularPixmap(self.avatar_path, 36))

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)
        text_layout.setAlignment(Qt.AlignVCenter)

        name_label = QLabel(self.user_name)
        name_label.setObjectName("user_name")
        name_label.setAlignment(Qt.AlignVCenter)
        role_label = QLabel(self.user_role)
        role_label.setObjectName("user_role")
        role_label.setAlignment(Qt.AlignVCenter)

        text_layout.addWidget(name_label)
        text_layout.addWidget(role_label)

        profile_layout.addWidget(self.avatar_label, alignment=Qt.AlignVCenter)
        profile_layout.addLayout(text_layout)
        profile_layout.setAlignment(text_layout, Qt.AlignVCenter)

        container_widget_layout.addWidget(bell_container, alignment=Qt.AlignVCenter)
        container_widget_layout.addWidget(profile_widget, alignment=Qt.AlignVCenter)

        main_layout.addWidget(container_widget, alignment=Qt.AlignVCenter)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)

        self.setstylesheet()

    def circularPixmap(self, path, size):
        source = QPixmap(path)
        if source.isNull():
            source = QPixmap(size, size)
            source.fill(QColor("#7C6EF8"))

        source = source.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path_ = QPainterPath()
        path_.addEllipse(0, 0, size, size)
        painter.setClipPath(path_)
        painter.drawPixmap(0, 0, source)
        painter.end()

        return rounded

    def setstylesheet(self):
        self.setStyleSheet("""
            QFrame#top_bar{
                background: #FFFFFF;
            }
            QPushButton#bell_button{
                background: transparent;
                border: none;
                font-size: 16px;
            }
            QLabel#badge{
                background: #EF4444;
                color: #FFFFFF;
                border-radius: 8px;
                font-size: 10px;
                font-weight: 600;
                font-family: 'Segoe UI';
            }
            QLabel#user_name{
                color: #1F2937;
                font-size: 13px;
                font-weight: 600;
                font-family: 'Segoe UI';
                background: transparent;
                border: none;
            }
            QLabel#user_role{
                color: #9CA3AF;
                font-size: 11px;
                font-family: 'Segoe UI';
                background: transparent;
                border: none;
            }
        """)