from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from components.avatar import Avatar
from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    FONT_FAMILY,
    COLOR_BORDER,
    COLOR_TEXT_MUTED,
)

COLOR_SURFACE_SOFT = "#F9FAFB"
COLOR_SUCCESS_BG = "#ECFDF3"
COLOR_SUCCESS_TEXT = "#027A48"
COLOR_WARNING_BG = "#FFFAEB"
COLOR_WARNING_TEXT = "#B54708"

class MemberSummary(QFrame):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.setStylesheet()

    def initUi(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 20)

        container = QFrame()
        container.setObjectName("container")
        container.setMinimumWidth(420)

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(16, 24, 40, 30))
        container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(18)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(14)

        self.avatar = Avatar("Peter Mwangi")
        header_layout.addWidget(self.avatar)

        name_widget = QWidget()
        name_widget_layout = QVBoxLayout(name_widget)
        name_widget_layout.setContentsMargins(0, 0, 0, 0)
        name_widget_layout.setSpacing(2)

        self.name = QLabel("Peter Mwangi")
        self.name.setObjectName("name")

        self.description = QLabel("Member since Jan 03, 2023")
        self.description.setObjectName("description")

        name_widget_layout.addWidget(self.name)
        name_widget_layout.addWidget(self.description)

        self.status_badge = QLabel("Active")
        self.status_badge.setObjectName("badge")
        self.status_badge.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(name_widget)
        header_layout.addStretch()
        header_layout.addWidget(self.status_badge, 0, Qt.AlignTop)

        container_layout.addWidget(header)
        container_layout.addWidget(self._make_divider())

        container_layout.addWidget(self._make_section_title("Member Details"))

        self.phone_number = self._make_value("0758731900")
        self.email = self._make_value("ondorajoshua75@gmail.com")
        self.id_number = self._make_value("39282892")
        self.next_of_kin = self._make_value("David Mochama - 0773994979")

        container_layout.addLayout(
            self._make_detail_grid(
                [
                    ("Phone", self.phone_number),
                    ("Email", self.email),
                    ("ID / Passport no.", self.id_number),
                    ("Next of kin", self.next_of_kin),
                ]
            )
        )

        container_layout.addWidget(self._make_divider())

        container_layout.addWidget(self._make_section_title("Contribution Summary"))

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        tile_1, self.total_contribution = self._make_stat_tile(
            "Total Contributions", "KES 48,000", "statValue"
        )
        tile_2, self.last_contribution = self._make_stat_tile(
            "Last Contribution", "KES 2,500", "statValue"
        )
        tile_3, self.loan = self._make_stat_tile("Loan", "KES 500", "statValueWarn")

        stats_layout.addWidget(tile_1)
        stats_layout.addWidget(tile_2)
        stats_layout.addWidget(tile_3)

        container_layout.addLayout(stats_layout)
        container_layout.addStretch()

        main_layout.addWidget(container)

    def _make_section_title(self, text):
        label = QLabel(text)
        label.setObjectName("sectionTitle")
        return label

    def _make_divider(self):
        line = QFrame()
        line.setObjectName("divider")
        line.setFixedHeight(1)
        return line

    def _make_value(self, text):
        label = QLabel(text)
        label.setObjectName("value")
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        return label

    def _make_detail_grid(self, rows):
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(12)
        grid.setColumnMinimumWidth(0, 130)
        grid.setColumnStretch(1, 1)

        for row, (key_text, value_label) in enumerate(rows):
            key = QLabel(key_text)
            key.setObjectName("key")
            grid.addWidget(key, row, 0)
            grid.addWidget(value_label, row, 1)
        return grid

    def _make_stat_tile(self, title, value, value_object_name):
        tile = QFrame()
        tile.setObjectName("statTile")

        layout = QVBoxLayout(tile)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setObjectName("statLabel")
        title_label.setWordWrap(True)

        value_label = QLabel(value)
        value_label.setObjectName(value_object_name)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return tile, value_label

    def set_member(self, name, member_since, phone, email, id_number,
                   next_of_kin, total, last, loan, status="Active"):
        self.name.setText(name)
        self.description.setText(f"Member since {member_since}")
        self.phone_number.setText(phone)
        self.email.setText(email)
        self.id_number.setText(id_number)
        self.next_of_kin.setText(next_of_kin)
        self.total_contribution.setText(total)
        self.last_contribution.setText(last)
        self.loan.setText(loan)
        self.status_badge.setText(status)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QFrame#container {{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_BORDER};
                border-radius: 16px;
            }}

            QLabel {{
                font-family: {FONT_FAMILY};
                background: transparent;
            }}

            QLabel#name {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 18px;
                font-weight: 700;
            }}
            QLabel#description {{
                color: {COLOR_TEXT_MUTED};
                font-size: 12px;
            }}

            QLabel#badge {{
                background-color: {COLOR_SUCCESS_BG};
                color: {COLOR_SUCCESS_TEXT};
                font-size: 12px;
                font-weight: 600;
                padding: 4px 12px;
                border-radius: 11px;
            }}

            QLabel#sectionTitle {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 14px;
                font-weight: 600;
            }}
            QLabel#key {{
                color: {COLOR_TEXT_MUTED};
                font-size: 13px;
            }}
            QLabel#value {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 13px;
                font-weight: 500;
            }}

            QFrame#divider {{
                background-color: {COLOR_BORDER};
                border: none;
            }}

            QFrame#statTile {{
                background-color: {COLOR_SURFACE_SOFT};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
            QLabel#statLabel {{
                color: {COLOR_TEXT_MUTED};
                font-size: 11px;
            }}
            QLabel#statValue {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 15px;
                font-weight: 700;
            }}
            QLabel#statValueWarn {{
                color: {COLOR_WARNING_TEXT};
                font-size: 15px;
                font-weight: 700;
            }}
        """)
