from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from components.form_dropdown import FormDropdown
from components.style_constants import FONT_FAMILY


class OfficialsInput(QWidget):
    selection_changed = pyqtSignal()

    def __init__(self, header):
        super().__init__()
        self.header = header
        self._members = {}
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        header = QLabel(self.header)
        header.setObjectName("header")

        self.combo = FormDropdown(
            "Select an official",
            [],
            height=40,
            icon_path="resources/down_arrow.svg",
        )
        self.combo.currentIndexChanged.connect(lambda _: self.selection_changed.emit())

        main_layout.addWidget(header)
        main_layout.addWidget(self.combo)

    def set_members(self, members):
        self._members = {m["id"]: m for m in members}
        self.combo.blockSignals(True)
        self.combo.clear()
        self.combo.addItem("Select an official", None)
        for m in members:
            self.combo.addItem(m["name"], m["id"])
        self.combo.setCurrentIndex(0)
        self.combo.blockSignals(False)

    def set_selected_id(self, member_id):
        idx = self.combo.findData(member_id) if member_id is not None else -1
        self.combo.blockSignals(True)
        self.combo.setCurrentIndex(idx if idx >= 0 else 0)
        self.combo.blockSignals(False)

    def selected_member(self):
        return self._members.get(self.combo.currentData())

    def selected_id(self):
        return self.combo.currentData()

    def set_disabled_ids(self, ids):
        model = self.combo.model()
        for i in range(1, self.combo.count()):
            item = model.item(i)
            if item is not None:
                item.setEnabled(self.combo.itemData(i) not in ids)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#header{{
                font-family: {FONT_FAMILY};
                font-size: 14px;
            }}
        """)
