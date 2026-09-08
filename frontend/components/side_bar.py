from PyQt5.QtWidgets import QFrame, QVBoxLayout, QButtonGroup, QWidget
from PyQt5.QtCore import pyqtSignal
from typing import Optional, List, Tuple

from components.menu_btn import MenuBtn


class SideBar(QFrame):
    menu_selected = pyqtSignal(str)

    MENU_ITEMS: List[Tuple[str, str]] = [
        ("Home", "resources/home.svg"),
        ("Employees", "resources/group.svg")
    ]

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFixedWidth(220)
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)
        self._init_ui()
        self._apply_stylesheet()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(2)

        for index, (label, icon_path) in enumerate(self.MENU_ITEMS):
            btn = MenuBtn(label, icon_path)
            self._button_group.addButton(btn, index)
            layout.addWidget(btn)

        layout.addStretch()

        if self._button_group.buttons():
            self._button_group.buttons()[0].setChecked(True)

        self._button_group.buttonClicked.connect(self._on_button_clicked)

    def _on_button_clicked(self, button: MenuBtn) -> None:
        self.menu_selected.emit(button.text())

    def _apply_stylesheet(self) -> None:
        self.setStyleSheet("""
            QFrame {
                background-color: #000000;
            }
        """)