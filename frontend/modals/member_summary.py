from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

from widgets.widget_12 import MemberSummary as MemberSummaryWidget
from api.api_client import ApiWorker


def _results(data):
    """Unwrap paginated ({'results': [...]}) or plain list responses."""
    if isinstance(data, dict):
        return data.get("results", [])
    return data or []


def _member_id(official):
    """Member id from an official record (nested object or plain id)."""
    m = official.get("member")
    return m.get("id") if isinstance(m, dict) else m


def _member_name(m):
    """Best-effort display name from a member record."""
    if not isinstance(m, dict):
        return str(m)
    user = m.get("user") if isinstance(m.get("user"), dict) else {}
    name = (
        m.get("name")
        or m.get("full_name")
        or f"{m.get('first_name', '')} {m.get('last_name', '')}".strip()
        or f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        or m.get("email")
        or "Unknown"
    )
    return name


def _office_label(official):
    """Office title for an official record (e.g. Chairperson)."""
    for key in ("office_display", "office", "role", "position", "title"):
        val = official.get(key)
        if isinstance(val, dict):
            val = val.get("name") or val.get("title")
        if val:
            return str(val).replace("_", " ").title()
    return ""


def build_member_rows(members_data, officials_data):
    members = _results(members_data)
    officials = _results(officials_data)

    # member id -> office title (only for officials that actually have one)
    offices = {}
    for off in officials:
        mid = _member_id(off)
        label = _office_label(off)
        if mid is not None and label:
            offices[mid] = label

    rows = []
    for m in members:
        # No officials set -> offices is empty -> everyone is a plain member
        rows.append({
            "name": _member_name(m),
            "role": offices.get(m.get("id"), ""),
        })

    # Officials first, then everyone else alphabetically
    rows.sort(key=lambda r: (r["role"] == "", r["role"], r["name"].lower()))
    return rows


class MemberSummaryDialog(QDialog):
    def __init__(self, api_client, chama_id, chama_name="", parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.chama_id = chama_id

        self.setWindowTitle("Member Summary")
        self.resize(420, 320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.status_label = QLabel("Loading members…")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.summary = MemberSummaryWidget()
        self.summary.set_title(chama_name)
        self.summary.hide()
        layout.addWidget(self.summary)

        self._load()

    def _fetch(self):
        members = self.api_client.list_members(self.chama_id)
        officials = self.api_client.list_officials(self.chama_id)
        return build_member_rows(members, officials)

    def _load(self):
        self.worker = ApiWorker(self._fetch)
        self.worker.success.connect(self._on_loaded)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_loaded(self, rows):
        if not rows:
            self.status_label.setText("This chama has no members yet.")
            return
        self.status_label.hide()
        self.summary.set_members(rows)
        self.summary.show()

    def _on_error(self, message):
        self.status_label.setText(f"Could not load members:\n{message}")
