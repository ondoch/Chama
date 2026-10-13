from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from api.api_client import ApiWorker, ApiError
from components.banner import Banner
from components.search_input import SearchInput
from components.form_dropdown import FormDropdown
from components.custom_table import CustomTable
from components.status_badge import StatusBadge
from components.style_constants import COLOR_BORDER, FONT_FAMILY, COLOR_TEXT_MUTED


class Widget5(QFrame):
    ROLE_OPTIONS = ["Treasurer", "Chair", "Secretary"]

    def __init__(self, api_client, employee_id=None):
        super().__init__()
        self.api = api_client
        self.employee_id = employee_id
        self.all_chamas = []
        self._roles = {}
        self._workers = []
        self._load_token = 0
        self._busy = False

        self.initUI()
        self.setStylesheet()
        self.load_chamas()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container.setObjectName("container")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        banner = Banner(
            "resources/chama.svg",
            "Chama Assignments",
            "Assign employee to specific chamas.",
        )

        search_container = QWidget()
        search_container_layout = QHBoxLayout(search_container)

        search_input = SearchInput("Search...")
        drop_down = FormDropdown(
            "Select a chama...",
            ["Mwangaza Women Chama", "Tumaini Group", "Upendo Chama"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )

        search_container_layout.addWidget(search_input, alignment=Qt.AlignLeft)
        search_container_layout.addWidget(drop_down, alignment=Qt.AlignRight)

        header_1 = QLabel("Available Chamas")
        header_1.setObjectName("header_1")

        self.table_1 = CustomTable([
            {
                "header": "",
                "type": "checkbox",
                "key": "selected",
                "width": 40,
                "on_toggle": self.on_chama_toggled,
            },
            {"header": "Chama Name", "type": "text", "key": "name"},
            {"header": "Members", "type": "text", "key": "members", "center": True},
            {
                "header": "Status",
                "key": "status",
                "factory": lambda value, row: StatusBadge(value),
            },
        ])

        header_2 = QLabel("Role in Chamas")
        header_2.setObjectName("header_2")

        sub_header = QLabel("Define what this employee will do in each assigned chama")
        sub_header.setObjectName("sub_header")

        self.table_2 = CustomTable([
            {"header": "Chama Name", "type": "text", "key": "name"},
            {
                "header": "Role in chama",
                "key": "role",
                "factory": self._make_role_dropdown,
            },
            {
                "header": "Actions",
                "type": "actions",
                "actions": [
                    ("Remove", self.remove_member),
                ],
            },
        ])

        container_layout.addWidget(banner, alignment=Qt.AlignLeft)
        container_layout.addWidget(search_container)
        container_layout.addWidget(header_1)
        container_layout.addWidget(self.table_1)
        container_layout.addWidget(header_2)
        container_layout.addWidget(sub_header)
        container_layout.addWidget(self.table_2)
        main_layout.addWidget(container)

        self.setLayout(main_layout)

        self._refresh_tables()

    def _run(self, fn, on_success, on_error, *args, **kwargs):
        worker = ApiWorker(fn, *args, **kwargs)
        worker.success.connect(on_success)
        worker.error.connect(on_error)
        worker.finished.connect(
            lambda w=worker: self._workers.remove(w) if w in self._workers else None
        )
        self._workers.append(worker)
        worker.start()

    def _show_error(self, message):
        QMessageBox.warning(self, "Chama Assignments", message)

    def wait_for_workers(self, timeout_ms=5000):
        for worker in list(self._workers):
            worker.wait(timeout_ms)

    def set_employee_id(self, employee_id):
        self.employee_id = employee_id
        self.load_chamas()

    @staticmethod
    def _results(data):
        if isinstance(data, dict):
            return data.get("results", [])
        return data or []

    def _to_row(self, chama, selected):
        chama_id = chama["public_id"]
        return {
            "id": chama_id,
            "name": chama.get("chama_name", ""),
            "members": chama.get("member_count", 0),
            "status": str(chama.get("status", "")).title(),
            "selected": selected,
            "role": self._roles.get(chama_id),
        }

    def load_chamas(self):
        self._load_token += 1
        token = self._load_token
        employee_id = self.employee_id

        def fetch():
            available = self.api.list_chamas(page=None, status="onboarding", unassigned=True)
            mine = (
                self.api.list_chamas(page=None, assigned_to=employee_id)
                if employee_id else []
            )
            return {"available": available, "mine": mine}

        self._run(
            fetch,
            lambda data, t=token: self._on_chamas_loaded(data, t),
            self._show_error,
        )

    def _on_chamas_loaded(self, data, token=None):
        if token is not None and token != self._load_token:
            return

        mine = [self._to_row(c, True) for c in self._results(data.get("mine"))]
        mine_ids = {c["id"] for c in mine}
        available = [
            self._to_row(c, False)
            for c in self._results(data.get("available"))
            if c["public_id"] not in mine_ids
        ]
        self.all_chamas = mine + available
        self._refresh_tables()

    def _live_action(self, fn, *args):
        if self._busy:
            self._refresh_tables()
            return
        self._busy = True

        def done(_):
            self._busy = False
            self.load_chamas()

        def failed(message):
            self._busy = False
            self._show_error(message)
            self.load_chamas()

        self._run(fn, done, failed, *args)

    def assign_selected(self, employee_id, on_done=None, reload=True):
        chosen = [dict(c) for c in self.all_chamas if c["selected"]]

        def assign_all():
            failed = []
            for c in chosen:
                try:
                    self.api.assign_chama(c["id"], employee_id)
                except ApiError as e:
                    failed.append(f'{c["name"]}: {e.message}')
            return failed

        def finished(failed):
            self.employee_id = employee_id
            if reload:
                self.load_chamas()
            if failed:
                QMessageBox.warning(
                    self, "Some chamas were not assigned", "\n".join(failed)
                )
            if on_done:
                on_done(failed)

        if not chosen:
            finished([])
            return

        self._run(assign_all, finished, self._show_error)

    def on_chama_toggled(self, row_data, checked):
        if self.employee_id is None:
            row_data["selected"] = checked
            self._refresh_tables()
        elif checked:
            self._live_action(self.api.assign_chama, row_data["id"], self.employee_id)
        else:
            self._refresh_tables()

    def remove_member(self, row):
        chama_id = row.get("id")
        self._roles.pop(chama_id, None)

        if self.employee_id is None:
            for chama in self.all_chamas:
                if chama["id"] == chama_id:
                    chama["selected"] = False
                    chama["role"] = None
                    break
            self._refresh_tables()
        else:
            self._live_action(self.api.unassign_chama, chama_id, self.employee_id)

    def _refresh_tables(self):
        available = [c for c in self.all_chamas if not c["selected"]]
        assigned = [c for c in self.all_chamas if c["selected"]]
        self.table_1.populate(available)
        self.table_2.populate(assigned)

    def _make_role_dropdown(self, value, row):
        dropdown = FormDropdown(placeholder="Select role", items=self.ROLE_OPTIONS, height=30)
        if value:
            index = dropdown.findText(value)
            if index >= 0:
                dropdown.setCurrentIndex(index)
        dropdown.currentTextChanged.connect(
            lambda text, row=row: self._on_role_changed(row, text)
        )
        return dropdown

    def _on_role_changed(self, row, role):
        chama_id = row.get("id")
        self._roles[chama_id] = role
        for chama in self.all_chamas:
            if chama["id"] == chama_id:
                chama["role"] = role
                break

    def edit_member(self, row):
        print("edit", row)

    def getChamaCount(self):
        return len([c for c in self.all_chamas if c["selected"]])

    def getSelectedChamaIds(self):
        return [c["id"] for c in self.all_chamas if c["selected"]]

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#header_1, #header_2{{
                font-family: "Segoe UI";
                font-size: 15px;
                font-weight: 600;
                margin-left: 20px;
            }}
            QLabel#sub_header{{
                font-family: '{FONT_FAMILY}';
                font-size: 13px;
                font-weight: 400;
                color: {COLOR_TEXT_MUTED};
                background-color: transparent;
                margin-left: 20px;
            }}
        """)
