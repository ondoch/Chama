from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from components.custom_table import CustomTable
from components.action_buttons import ActionButtonGroup
from components.status_badge import StatusBadge
from components.progress_cell import ProgressCell
from components.facilitator_cell import FacilitatorCell
from components.style_constants import (
    FONT_FAMILY,
)


def actions_factory(actions_config):
    def factory(value, row_data):
        return ActionButtonGroup(actions_config, row_data=row_data)
    return factory


def make_name_cell(value, row_data):
    label = QLabel(str(value or ""))
    label.setStyleSheet(
        f"color: #1B2559; font-size: 14px; font-family: {FONT_FAMILY};"
        "background: transparent; border: none; padding-left: 8px;"
    )
    return label


def make_facilitator_cell(value, row_data):
    return FacilitatorCell(value, row_data.get("avatar"))


def make_progress_cell(value, row_data):
    return ProgressCell(value)


def make_status_cell(value, row_data):
    holder = QWidget()
    layout = QHBoxLayout(holder)
    layout.setContentsMargins(8, 0, 8, 0)
    layout.addWidget(StatusBadge(value or "inactive"), 0, Qt.AlignLeft | Qt.AlignVCenter)
    return holder


def build_columns(on_view=None):
    def view_clicked(row, btn=None):
        if on_view:
            on_view(row)
        else:
            print("View", row)

    return [
        {"header": "Chama name", "key": "chama_name", "width": 175,
         "factory": make_name_cell},
        {"header": "Facilitator", "key": "facilitator", "width": 165,
         "factory": make_facilitator_cell},
        {"header": "Progress", "key": "progress", "factory": make_progress_cell},
        {"header": "Status", "key": "status", "width": 115,
         "factory": make_status_cell},
        {"header": "Started", "key": "started", "width": 105},
        {"header": "Actions", "key": None, "width": 100,
         "factory": actions_factory([
             {"label": "View", "width": 60, "callback": view_clicked},
         ])},
    ]


class OnboardingTable(CustomTable):
    ROW_HEIGHT = 52
    COMPACT_BELOW = 800

    def __init__(self, on_view=None):
        super().__init__(build_columns(on_view))

        self._started_col = next(
            i for i, col in enumerate(self.columns) if col.get("key") == "started"
        )
        self._compact = False

        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        header = self.table.horizontalHeader()
        header.setMinimumSectionSize(90)
        header.setHighlightSections(False)

        self.setStyleSheet(self.styleSheet() + """
            QTableWidget {
                border: 1px solid #DCE3F5;
                border-radius: 12px;
            }
            QHeaderView::section {
                background-color: #F3F6FD;
                color: #1B2559;
            }
        """)

    FULL_WIDTHS = [175, 165, None, 115, 105, 100]
    COMPACT_WIDTHS = [162, 145, None, 105, None, 90]

    def set_compact(self, compact: bool):
        self._compact = compact
        self.table.setColumnHidden(self._started_col, compact)
        widths = self.COMPACT_WIDTHS if compact else self.FULL_WIDTHS
        for index, width in enumerate(widths):
            if width:
                self.table.setColumnWidth(index, width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = event.size().width()
        if not self._compact and width < self.COMPACT_BELOW:
            self.set_compact(True)
        elif self._compact and width > self.COMPACT_BELOW + 40:
            self.set_compact(False)
