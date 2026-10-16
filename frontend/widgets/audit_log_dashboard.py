import json
from datetime import datetime

from PyQt5.Qt import (
    QFrame,
    QWidget,
    QLabel,
    QDateEdit,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QDate, QLocale, QTimer
from PyQt5.QtGui import QPixmap

from api.api_client import ApiWorker
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

DEFAULT_PAGE_SIZE = 10     # used only until the table has been measured
MIN_PAGE_SIZE = 5
MAX_PAGE_SIZE = 100        # must match max_page_size on AuditLogPagination


class AuditLogDashboard(QFrame):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.page = 1
        self.page_size = DEFAULT_PAGE_SIZE
        self._loaded = False
        self._request_id = 0
        self._workers = set()

        self.initUi()
        self.setStylesheet()
        self.connect_signals()

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
        top_row_layout.setContentsMargins(0, 0, 0, 0)
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

        date_filter = QWidget()
        date_filter_layout = QHBoxLayout(date_filter)

        from_label = QLabel("From")
        from_label.setObjectName("filter_label")
        to_label = QLabel("To")
        to_label.setObjectName("filter_label")

        date_filter_layout.addWidget(from_label)
        date_filter_layout.addWidget(self.start_date)
        date_filter_layout.addWidget(to_label)
        date_filter_layout.addWidget(self.end_date)

        search_widget_layout.addWidget(self.search_email, alignment=Qt.AlignLeft)
        search_widget_layout.addWidget(date_filter, alignment=Qt.AlignRight)

        self.footer = Pagination(page_size=self.page_size, noun="logs")
        self.table = AuditLogTable(on_view=self.show_details)

        container_widget_layout.addWidget(top_row)
        container_widget_layout.addLayout(banner_layout)
        container_widget_layout.addWidget(search_widget)
        container_widget_layout.addWidget(self.table, stretch=1)
        container_widget_layout.addWidget(self.footer)

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

    def connect_signals(self):
        self._search_timer = QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(400)
        self._search_timer.timeout.connect(self.reset_and_load)

        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(250)
        self._resize_timer.timeout.connect(self.apply_page_size)

        self.search_email.textChanged.connect(lambda _text: self._search_timer.start())
        self.start_date.dateChanged.connect(lambda _d: self.reset_and_load())
        self.end_date.dateChanged.connect(lambda _d: self.reset_and_load())
        self.footer.page_changed.connect(self.go_to_page)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._loaded:
            self._loaded = True
            QTimer.singleShot(0, lambda: self.apply_page_size(force=True))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._loaded:
            self._resize_timer.start()

    def apply_page_size(self, force=False):
        fit = max(MIN_PAGE_SIZE, min(MAX_PAGE_SIZE, self.table.rows_that_fit()))
        if fit == self.page_size and not force:
            return

        first_index = (self.page - 1) * self.page_size
        self.page_size = fit
        self.page = first_index // fit + 1
        self.load_logs()

    def reset_and_load(self):
        self.page = 1
        self.load_logs()

    def go_to_page(self, page):
        self.page = page
        self.load_logs()

    def _date_value(self, edit):
        d = edit.date()
        return None if d == MIN_DATE else d.toString("yyyy-MM-dd")

    def load_logs(self):
        self._request_id += 1
        rid = self._request_id

        worker = ApiWorker(
            self.api_client.list_audit_logs,
            page=self.page,
            page_size=self.page_size,
            search=self.search_email.entry.text().strip(),
            date_from=self._date_value(self.start_date),
            date_to=self._date_value(self.end_date),
        )
        worker.success.connect(lambda data, rid=rid: self.on_loaded(rid, data))
        worker.error.connect(lambda msg, rid=rid: self.on_error(rid, msg))
        worker.finished.connect(lambda w=worker: self._workers.discard(w))

        self._workers.add(worker)
        worker.start()

    def on_loaded(self, rid, data):
        if rid != self._request_id:
            return

        if isinstance(data, dict):
            results = data.get("results", [])
            total = data.get("count", len(results))
        else:
            results = data or []
            total = len(results)

        if not results and total and self.page > 1:
            self.page = max(1, -(-total // self.page_size))
            self.load_logs()
            return

        self.table.populate([self._to_row(r) for r in results])
        self.footer.set_state(self.page, total, self.page_size)

    def on_error(self, rid, message):
        if rid != self._request_id:
            return
        QMessageBox.warning(self, "Audit Logs", message)

    @staticmethod
    def _to_row(r):
        created = r.get("created_at") or ""
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00")).astimezone()
            created = dt.strftime("%b. %d, %Y %H:%M")
        except ValueError:
            pass

        return {
            "id": r.get("id"),
            "actor": r.get("actor_email") or "System",
            "action": (r.get("action") or "").replace("_", " ").title(),
            "target_label": r.get("target_label") or "",
            "created_at": created,
            "raw_data": r,
        }

    def show_details(self, row):
        raw = row.get("raw_data", {})
        details = raw.get("details")
        body = (
            json.dumps(details, indent=2, default=str)
            if details else "No extra details recorded."
        )
        QMessageBox.information(
            self,
            f"{row.get('action', 'Audit')} - {row.get('actor', '')}",
            f"Target: {row.get('target_label') or '-'}\n"
            f"When: {row.get('created_at')}\n\n{body}",
        )

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
