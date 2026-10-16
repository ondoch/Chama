from PyQt5.Qt import (
    QFrame,
    QWidget,
    QLabel,
    QDateEdit,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import (
    Qt,
    QDate,
    QLocale
)
from PyQt5.QtGui import QPixmap

from components.banner_4 import Banner4
from components.search_input import SearchInput
from components.pagination import Pagination
from components.audit_log_table import AuditLogTable

from components.style_constants import (
    COLOR_BORDER,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    FONT_FAMILY,
)

DATE_DISPLAY_FORMAT = "MMM. d, yyyy"
MIN_DATE = QDate(2000, 1, 1) 

class AuditLogDashboard(QFrame):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.setStylesheet()

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container_widget = QWidget()
        container_widget.setObjectName("container_widget")
        container_widget_layout = QVBoxLayout(container_widget)

        header_widget = QWidget()
        header_widget_layout = QHBoxLayout(header_widget)
        header_widget_layout.setContentsMargins(20, 0, 0, 0)

        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(10, 0, 0, 0)
        header_widget_layout.setSpacing(0)

        icon = QLabel()
        icon.setFixedSize(50, 50)
        pixmap = QPixmap("resources/security.svg")
        icon.setPixmap(
            pixmap.scaled(49, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        header = QLabel("Audit Logs")
        header.setObjectName("header")
        label = QLabel("Track every important action performed in the system.")
        label.setObjectName("label")

        header_layout.addWidget(header)
        header_layout.addWidget(label)
        header_widget_layout.addWidget(icon)
        header_widget_layout.addLayout(header_layout)

        top_row = QWidget()
        top_row_layout = QHBoxLayout(top_row)
        top_row_layout.setContentsMargins(0,0,0,0)

        top_row_layout.addWidget(header_widget)

        banner_layout = QHBoxLayout()
        banner_layout.setSpacing(12)

        left, top, right, bottom = banner_layout.getContentsMargins()
        banner_layout.setContentsMargins(left, 10, right, bottom)

        self.banner_total_actions = Banner4(
            "resources/total_actions.svg", "0", "Total Actions"
        )
        self.banner_employees = Banner4(
            "resources/audit_user.svg", "0", "Employees"
        )
        self.banner_chamas = Banner4(
            "resources/users_chama.svg", "0", "Chamas"
        )
        self.banner_today = Banner4(
            "resources/today.svg", "0", "Today"
        )

        banner_layout.addWidget(self.banner_total_actions, stretch=1)
        banner_layout.addWidget(self.banner_employees, stretch=1)
        banner_layout.addWidget(self.banner_chamas, stretch=1)
        banner_layout.addWidget(self.banner_today, stretch=1)

        search_widget = QWidget()
        search_widget_layout = QHBoxLayout(search_widget)

        self.search_email = SearchInput("Search...")

        self.start_date = self.make_date_filter()

        self.end_date = self.make_date_filter()

        from_label = QLabel("From")
        from_label.setObjectName("filter_label")
        to_label = QLabel("To")
        to_label.setObjectName("filter_label")

        search_widget_layout.addWidget(self.search_email, alignment=Qt.AlignLeft)
        search_widget_layout.addWidget(from_label, alignment=Qt.AlignRight)
        search_widget_layout.addWidget(self.start_date, alignment=Qt.AlignRight)
        search_widget_layout.addWidget(to_label, alignment=Qt.AlignRight)
        search_widget_layout.addWidget(self.end_date, alignment=Qt.AlignRight)

        footer = Pagination()

        self.table = AuditLogTable()

        container_widget_layout.addWidget(top_row)
        container_widget_layout.addLayout(banner_layout)
        container_widget_layout.addWidget(search_widget)
        container_widget_layout.addWidget(self.table)
        container_widget_layout.addWidget(footer, alignment=Qt.AlignBottom)

        main_layout.addWidget(container_widget)

    def make_date_filter(self):
        edit = QDateEdit()
        edit.setLocale(QLocale(QLocale.English))
        edit.setDisplayFormat(DATE_DISPLAY_FORMAT)
        edit.setCalendarPopup(True)
        edit.setFixedHeight(40)
        edit.setMinimumWidth(150)
        edit.setMinimumDate(MIN_DATE)
        edit.setMaximumDate(QDate.currentDate().addYears(1))
        edit.setSpecialValueText("All")
        edit.setDate(MIN_DATE)
        return edit

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container_widget{{
                border: 1px solid {COLOR_BORDER};
                background-color: #FFFFFF;
                border-radius: 10px;
            }}
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 600;
            }}
            QLabel#label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 16px;
            }}
            QLabel#filter_label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 14px;
            }}
            QDateEdit{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
                padding: 0 10px;
                background-color: #FFFFFF;
            }}
            QDateEdit::drop-down{{
                border: none;
                width: 28px;
            }}
            QDateEdit::down-arrow{{
                image: url(resources/down_arrow.svg);
                width: 12px;
                height: 12px;
            }}
        """)
