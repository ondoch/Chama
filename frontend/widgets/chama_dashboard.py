from datetime import datetime
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QDialog,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from api.api_client import ApiWorker
from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
    COLOR_SIDEBAR_BG,
    COLOR_SIDEBAR_HOVER,
    COLOR_SIDEBAR_SELECT,
)
from components.search_input import SearchInput
from components.form_dropdown import FormDropdown
from components.groups_table import GroupsTable
from components.pagination import Pagination
from components.banner_4 import Banner4
from modals.chama_information import ChamaInformation

def format_date(iso):
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}"
    except ValueError:
        return str(iso)[:10]


def clean_number(value):
    return str(value).replace("KSh", "").replace("%", "").replace(",", "").strip()


def normalize_chama(c):
    return {
        "public_id": c.get("public_id"),
        "name": c.get("chama_name", ""),
        "description": c.get("description", ""),
        "contribution": f"KSh {c.get('contribution', '0')}",
        "pool_percentage": c.get("pool_percentage", ""),
        "registration_number": c.get("registration_number", ""),
        "meeting_frequency": c.get("meeting_frequency", ""),
        "share_percentage": c.get("share_percentage", ""),
        "loan_percentage": c.get("loan_percentage", ""),
        "created_on": format_date(c.get("created_at")),
        "status": str(c.get("status", "")).title(),
        "member_count": c.get("member_count", 0),
        "officials_count": 0,
        "pending_approvals": 0,
        "raw": c,
    }


def form_to_payload(values):
    return {
        "chama_name": values["chama_name"],
        "description": values["description"],
        "registration_number": values["registration_number"],
        "meeting_frequency": values["meeting_frequency"],
        "contribution": clean_number(values["contribution"]),
        "share_percentage": clean_number(values["share_percentage"]),
        "pool_percentage": clean_number(values["pool_percentage"]),
        "loan_percentage": clean_number(values["loan_percentage"]),
    }

class ChamaDashboard(QFrame):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.chamas = []
        self._workers = set()
        self.initUI()
        self.setStylesheet()
        self.updateBanners()
        self.loadChamas()

    def initUI(self):
        main_layout = QVBoxLayout(self)

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
        pixmap = QPixmap("resources/group_1.svg")
        icon.setPixmap(
            pixmap.scaled(49, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        header = QLabel("Groups")
        header.setObjectName("header")
        label = QLabel("View and manage all groups")
        label.setObjectName("label")

        header_layout.addWidget(header)
        header_layout.addWidget(label)
        header_widget_layout.addWidget(icon)
        header_widget_layout.addLayout(header_layout)

        self.add_chama_button = QPushButton("+ Add Chama")
        self.add_chama_button.setObjectName("add_chama_button")
        self.add_chama_button.setCursor(Qt.PointingHandCursor)
        self.add_chama_button.setFixedHeight(38)
        self.add_chama_button.clicked.connect(self.openAddChamaDialog)

        top_row_widget = QWidget()
        top_row_layout = QHBoxLayout(top_row_widget)
        top_row_layout.setContentsMargins(0, 0, 0, 0)

        top_row_layout.addWidget(header_widget, alignment=Qt.AlignLeft)
        top_row_layout.addStretch()
        top_row_layout.addWidget(
            self.add_chama_button, alignment=Qt.AlignRight | Qt.AlignVCenter
        )

        banner_layout = QHBoxLayout()
        banner_layout.setSpacing(12)

        left, top, right, bottom = banner_layout.getContentsMargins()
        banner_layout.setContentsMargins(left, 10, right, bottom)

        self.banner_total_chamas = Banner4(
            "resources/chamas.svg", "0", "Total Chamas", "0 Active"
        )
        self.banner_members = Banner4(
            "resources/people.svg", "0", "Members", "Across all"
        )
        self.banner_pending = Banner4(
            "resources/inactive_users.svg",
            "0",
            "Pending Approvals",
            "Waiting for confirmation",
        )
        self.banner_officials = Banner4(
            "resources/leader_1.svg",
            "0",
            "Chama Officials",
            "Across all chamas",
        )

        banner_layout.addWidget(self.banner_total_chamas, stretch=1)
        banner_layout.addWidget(self.banner_members, stretch=1)
        banner_layout.addWidget(self.banner_pending, stretch=1)
        banner_layout.addWidget(self.banner_officials, stretch=1)

        search_widget = QWidget()
        search_widget_layout = QHBoxLayout(search_widget)

        self.search = SearchInput("Search...")
        self.search.textChanged.connect(self.filterChamas)

        search_widget_layout.addWidget(self.search, alignment=Qt.AlignLeft)

        container_widget_layout.addWidget(top_row_widget)
        container_widget_layout.addLayout(banner_layout)
        container_widget_layout.addWidget(search_widget)

        self.table = GroupsTable()
        self.table.edit_requested.connect(self.editChama)
        self.table.close_requested.connect(self.closeChama)

        container_widget_layout.addWidget(self.table)

        footer = Pagination()
        container_widget_layout.addWidget(footer, alignment=Qt.AlignBottom)

        main_layout.addWidget(container_widget)

    def runWorker(self, fn, on_success, on_error=None, *args, **kwargs):
        worker = ApiWorker(fn, *args, **kwargs)
        self._workers.add(worker)
        worker.success.connect(on_success)
        worker.error.connect(on_error or self.showError)
        worker.finished.connect(lambda w=worker: self._workers.discard(w))
        worker.start()

    def showError(self, message):
        QMessageBox.warning(self, "Error", message)

    def loadChamas(self):
        self.runWorker(self.api.list_chamas, self.onChamasLoaded)

    def onChamasLoaded(self, data):
        if isinstance(data, dict):
            results = data.get("results", [])
        else:
            results = data or []
        self.chamas = [normalize_chama(c) for c in results]
        self.filterChamas(self.search.entry.text())
        self.updateBanners()

    def filterChamas(self, text=""):
        query = text.strip().lower()

        if not query:
            filtered = self.chamas
        else:
            filtered = [
                c
                for c in self.chamas
                if query in str(c.get("name", "")).lower()
                or query in str(c.get("description", "")).lower()
                or query in str(c.get("registration_number", "")).lower()
                or query in str(c.get("status", "")).lower()
            ]

        self.table.populate(filtered)

    def openAddChamaDialog(self):
        dialog = ChamaInformation(self)
        if dialog.exec_() == QDialog.Accepted:
            self.createChama(dialog.values)

    def createChama(self, values):
        self.add_chama_button.setEnabled(False)
        self.runWorker(
            self.api.create_chama,
            self.onChamaCreated,
            self.onCreateFailed,
            form_to_payload(values),
        )

    def onChamaCreated(self, data):
        self.add_chama_button.setEnabled(True)
        self.chamas.insert(0, normalize_chama(data))
        self.filterChamas(self.search.entry.text())
        self.updateBanners()

    def onCreateFailed(self, message):
        self.add_chama_button.setEnabled(True)
        self.showError(message)

    def editChama(self, row):
        dialog = ChamaInformation(self, chama=row.get("raw") or {})
        if dialog.exec_() != QDialog.Accepted:
            return
        self.runWorker(
            self.api.update_chama,
            self.onChamaUpdated,
            None,
            row["public_id"],
            form_to_payload(dialog.values),
        )

    def onChamaUpdated(self, data):
        updated = normalize_chama(data)
        for i, c in enumerate(self.chamas):
            if c["public_id"] == updated["public_id"]:
                self.chamas[i] = updated
                break
        self.filterChamas(self.search.entry.text())
        self.updateBanners()

    def changeStatus(self, row, new_status, reason=""):
        self.runWorker(
            self.api.set_chama_status,
            self.onChamaUpdated,
            None,
            row["public_id"],
            new_status,
            reason,
        )

    def closeChama(self, row):
        self.changeStatus(row, "closed", "Closed from desktop app")

    def updateBanners(self):
        total_chamas = len(self.chamas)
        active_chamas = sum(
            1 for c in self.chamas if c.get("status") == "Active"
        )
        total_members = sum(c.get("member_count", 0) for c in self.chamas)
        total_officials = sum(c.get("officials_count", 0) for c in self.chamas)
        total_pending = sum(c.get("pending_approvals", 0) for c in self.chamas)

        self.banner_total_chamas.setHeader(total_chamas)
        self.banner_total_chamas.setSubHeader2(f"{active_chamas} Active")
        self.banner_members.setHeader(total_members)
        self.banner_pending.setHeader(total_pending)
        self.banner_officials.setHeader(total_officials)

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
            QPushButton#add_chama_button{{
                font-family: {FONT_FAMILY};
                background-color: {COLOR_SIDEBAR_BG};
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 600;
                border: none;
                border-radius: 6px;
                padding: 0 16px;
            }}
            QPushButton#add_chama_button:hover{{
                background: {COLOR_SIDEBAR_HOVER};
            }}
            QPushButton#add_chama_button:pressed{{
                background: {COLOR_SIDEBAR_SELECT};
            }}
        """)
