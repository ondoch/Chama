from typing import List, Tuple, Optional

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QButtonGroup, QLabel, QWidget
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal

from components.menu_btn import MenuBtn
from components.divider import Divider
from components.style_constants import COLOR_SIDEBAR_BG, COLOR_SECTION_LABEL


class Sidebar(QFrame):
    menu_selected = pyqtSignal(str)
    menu_index_selected = pyqtSignal(int)
    logout_clicked = pyqtSignal()

    MENU_SECTIONS: List[Tuple[Optional[str], List[Tuple[str, str]]]] = [
        (None, [
            ("Dashboard", "resources/dashboard.svg"),
        ]),
        ("Management", [
            ("Chamas", "resources/user_groups.svg"),
            ("Employees", "resources/user_svg.svg"),
        ]),
        ("Operations", [
            ("Onboarding", "resources/onboarding.svg"),
            ("Assignments", "resources/assignments.svg"),
            ("Reports", "resources/reports.svg"),
        ]),
        ("Security", [
            ("Audit logs", "resources/audit_logs.svg"),
        ]),
    ]

    def __init__(self, app_name: str = "Chama Manager", logo_icon_path: Optional[str] = None,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.app_name = app_name
        self.logo_icon_path = logo_icon_path
        self.setFixedWidth(240)
        self.setStyleSheet(f"background:{COLOR_SIDEBAR_BG}; border-right:1px solid #E4E6EC;")
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)
        self.initUI()

    def initUI(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 12)
        layout.setSpacing(2)

        layout.addLayout(self._build_header())

        flat_index = 0
        for i, (section_title, items) in enumerate(self.MENU_SECTIONS):
            if section_title:
                layout.addWidget(self._build_section_label(section_title))
            for label, icon_path in items:
                btn = MenuBtn(label, icon_path=icon_path)
                self._button_group.addButton(btn, flat_index)
                self._wrap(layout, btn)
                flat_index += 1

            if i < len(self.MENU_SECTIONS) - 1:
                layout.addWidget(Divider())

        if self._button_group.buttons():
            self._button_group.buttons()[0].setChecked(True)
        self._button_group.buttonClicked.connect(self._on_button_clicked)

        layout.addStretch()

        layout.addWidget(Divider())
        logout_btn = MenuBtn("Log out", icon_path="resources/logout.svg")
        logout_btn.setCheckable(False)
        logout_btn.clicked.connect(self.logout_clicked.emit)
        self._wrap(layout, logout_btn)

    def _on_button_clicked(self, button: MenuBtn) -> None:
        self.menu_selected.emit(button.text())
        self.menu_index_selected.emit(self._button_group.id(button))

    def _build_header(self) -> QHBoxLayout:
        header = QHBoxLayout()
        header.setContentsMargins(16, 4, 16, 16)

        logo = QLabel()
        if self.logo_icon_path:
            logo.setPixmap(QIcon(self.logo_icon_path).pixmap(20, 20))

        title = QLabel(f"<b>{self.app_name}</b>")
        title.setStyleSheet("font-size:15px; color:#1F2430;")

        header.addWidget(logo)
        header.addWidget(title)
        header.addStretch()
        return header

    @staticmethod
    def _build_section_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(
            f"color:{COLOR_SECTION_LABEL}; font-size:11px; font-weight:600; "
            f"padding: 10px 16px 4px 16px;"
        )
        return label

    @staticmethod
    def _wrap(layout: QVBoxLayout, widget: QWidget) -> None:
        row = QHBoxLayout()
        row.setContentsMargins(10, 1, 10, 1)
        row.addWidget(widget)
        layout.addLayout(row)
