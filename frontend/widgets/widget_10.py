from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from components.officials_input import OfficialsInput
from components.banner_3 import Banner3
from components.style_constants import (
    COLOR_BORDER,
    FONT_FAMILY,
    COLOR_TEXT_PRIMARY
)


class Official(QWidget):
    officials_changed = pyqtSignal(dict)
    POSITIONS = ("Chairperson", "Secretary", "Treasurer")

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        container_widget = QWidget()
        container_widget.setFixedWidth(300)
        container_widget.setObjectName("overall_container")
        container_widget_layout = QVBoxLayout(container_widget)

        header_container = QWidget()
        header_container_layout = QHBoxLayout(header_container)

        icon = QLabel()
        icon.setFixedSize(45, 45)
        pixmap = QPixmap("resources/leader.svg")
        icon.setPixmap(pixmap.scaled(43, 43, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        banner = Banner3()

        header_label = QLabel("Assign chama officials")
        header_label.setObjectName("header_label")

        header_container_layout.addWidget(icon)
        header_container_layout.addWidget(header_label)

        main_layout.setAlignment(Qt.AlignCenter)

        self.inputs = {pos: OfficialsInput(pos) for pos in self.POSITIONS}
        for inp in self.inputs.values():
            inp.selection_changed.connect(self._on_selection_changed)

        container_widget_layout.addWidget(banner)
        container_widget_layout.addWidget(header_container)
        for inp in self.inputs.values():
            container_widget_layout.addWidget(inp)

        main_layout.addWidget(container_widget)

    def set_members(self, members):
        for inp in self.inputs.values():
            inp.set_members(members)
        self._on_selection_changed()

    def set_selected(self, ids_by_position):
        for pos, inp in self.inputs.items():
            inp.set_selected_id(ids_by_position.get(pos.lower()))
        self._on_selection_changed()

    def selected_officials(self):
        return {pos: inp.selected_member() for pos, inp in self.inputs.items()}

    def selected_ids(self):
        return {pos.lower(): inp.selected_id() for pos, inp in self.inputs.items()}

    def _on_selection_changed(self):
        chosen = {pos: inp.selected_id() for pos, inp in self.inputs.items()}
        for pos, inp in self.inputs.items():
            taken = {mid for p, mid in chosen.items() if p != pos and mid is not None}
            inp.set_disabled_ids(taken)
        self.officials_changed.emit(self.selected_officials())

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#overall_container{{
                border: 1px solid {COLOR_BORDER};
                border-radius: 6px
            }}
            QLabel#header_label{{
                font-family: '{FONT_FAMILY}';
                font-size: 16px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
        """)
