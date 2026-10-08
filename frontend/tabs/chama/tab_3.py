from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon

from api.api_client import ApiWorker, APIClient
from widgets.widget_9 import MembersTable, normalize_member
from widgets.widget_10 import Official
from widgets.widget_11 import SummaryWidget
from components.banner import Banner
from components.style_constants import (
    COLOR_CARD_BG,
    COLOR_BORDER,
    COLOR_ACCENT_BLUE
)


class Tab3(QFrame):
    cancel_clicked = pyqtSignal()
    finish_clicked = pyqtSignal()

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.chama = None
        self.chama_pk = None
        self._request_id = 0
        self._worker = None
        self._officials_worker = None
        self._save_worker = None
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container_widget = QWidget()
        container_widget.setFixedWidth(1100)
        container_widget.setObjectName("container")
        container_widget_layout = QVBoxLayout(container_widget)

        banner = Banner(
            "resources/group_svg.svg",
            "Set Officials",
            "Choose the chama's chairperson, secretary and treasurer",
        )
        container_widget_layout.addWidget(banner, alignment=Qt.AlignLeft)

        row_container = QWidget()
        row_container_layout = QHBoxLayout(row_container)
        row_container_layout.setSpacing(15)

        row_1 = QVBoxLayout()
        row_2 = QVBoxLayout()
        row_3 = QVBoxLayout()

        self.members_table = MembersTable()
        self.officials = Official()
        self.summary = SummaryWidget()
        self.officials.officials_changed.connect(self.summary.set_officials)

        row_1.addWidget(self.members_table)
        row_2.addWidget(self.officials)
        row_3.addWidget(self.summary)
        row_3.addStretch()

        row_container_layout.addLayout(row_1)
        row_container_layout.addLayout(row_2)
        row_container_layout.addLayout(row_3)

        nav_row = QHBoxLayout()
        nav_row.setContentsMargins(10, 0, 10, 0)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(QIcon("resources/cancel.svg"))
        self.cancel_btn.setIconSize(QSize(16, 16))
        self.cancel_btn.setLayoutDirection(Qt.LeftToRight)
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.setStyleSheet(
            f"padding: 8px 16px; border:1px solid {COLOR_ACCENT_BLUE}; color: #000; border-radius: 6px"
        )

        self.finish_btn = QPushButton("Finish")
        self.finish_btn.setIcon(QIcon("resources/tick.svg"))
        self.finish_btn.setIconSize(QSize(16, 16))
        self.finish_btn.setLayoutDirection(Qt.RightToLeft)
        self.finish_btn.setMinimumWidth(100)
        self.finish_btn.setStyleSheet(
            f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px"
        )

        for btn in (self.cancel_btn, self.finish_btn):
            btn.setCursor(Qt.PointingHandCursor)

        self.cancel_btn.clicked.connect(self.cancel_clicked.emit)
        self.finish_btn.clicked.connect(self._save)

        nav_row.addWidget(self.cancel_btn)
        nav_row.addStretch()
        nav_row.addWidget(self.finish_btn)

        container_widget_layout.addWidget(row_container)
        container_widget_layout.addLayout(nav_row)

        main_layout.addStretch()
        main_layout.addWidget(container_widget, alignment=Qt.AlignHCenter)
        main_layout.addStretch()

    def load_chama(self, row_data):
        self.chama = row_data
        self.chama_pk = row_data.get("public_id")   # used for members AND officials URLs
        self.summary.set_chama(row_data.get("name", ""))
        self._apply_members([])

        self._request_id += 1
        rid = self._request_id
        self._worker = ApiWorker(self.api_client.list_members, self.chama_pk)
        self._worker.success.connect(lambda data, r=rid: self._on_members(r, data))
        self._worker.error.connect(lambda msg, r=rid: self._on_load_error(r, msg))
        self._worker.start()

    def _on_members(self, request_id, data):
        if request_id != self._request_id:
            return
        if isinstance(data, dict):
            data = data.get("results", [])
        self._apply_members([normalize_member(m) for m in (data or [])])

        self._officials_worker = ApiWorker(self.api_client.list_officials, self.chama_pk)
        self._officials_worker.success.connect(lambda d, r=request_id: self._on_officials(r, d))
        self._officials_worker.error.connect(lambda msg, r=request_id: self._on_load_error(r, msg))
        self._officials_worker.start()

    def _on_officials(self, request_id, data):
        if request_id != self._request_id:
            return
        current = APIClient._results(data)
        ids = {
            o["position"]: APIClient._member_id(o)
            for o in current if not o.get("ended_on")
        }
        self.officials.set_selected(ids)

    def _on_load_error(self, request_id, message):
        if request_id != self._request_id:
            return
        QMessageBox.warning(self, "Could not load data", message)

    def _apply_members(self, members):
        self.members_table.set_members(members)
        self.officials.set_members(members)
        self.summary.set_members_count(len(members))

    def selected_officials(self):
        return self.officials.selected_officials()

    def _save(self):
        if self.chama_pk is None:
            return
        selection = self.officials.selected_ids()
        self.finish_btn.setEnabled(False)
        self._save_worker = ApiWorker(self.api_client.save_officials, self.chama_pk, selection)
        self._save_worker.success.connect(self._on_saved)
        self._save_worker.error.connect(self._on_save_error)
        self._save_worker.start()

    def _on_saved(self, _result):
        self.finish_btn.setEnabled(True)
        self.finish_clicked.emit()

    def _on_save_error(self, message):
        self.finish_btn.setEnabled(True)
        QMessageBox.warning(self, "Could not save officials", message)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container{{
                background: {COLOR_CARD_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
            }}
        """)
