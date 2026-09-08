from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QHBoxLayout,
    QCheckBox,
    QComboBox,
    QPushButton,
)
from PyQt5.QtCore import Qt


class CustomTable(QWidget):
    def __init__(self, columns: list):
        super().__init__()

        self.columns = columns

        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(
            [col["header"] for col in self.columns]
        )

        header = self.table.horizontalHeader()
        for i, col in enumerate(self.columns):
            if col.get("width"):
                header.setSectionResizeMode(i, QHeaderView.Fixed)
                self.table.setColumnWidth(i, col["width"])
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setRowCount(0)

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QTableWidget {{
                border: 1px solid #d9d9d9;
                border-radius: 8px;
                gridline-color: #eeeeee;
                padding: 4px;
                font-family: "Segoe UI";
                font-size: 14px;
            }}
            QHeaderView::section {{
                background-color: #f0f0f0;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-family: "Segoe UI";
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 6px;
                font-family: "Segoe UI";
            }}

            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 10px;
                margin: 4px 2px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #c4c4c4;
                border-radius: 5px;
                min-height: 24px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #a6a6a6;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}

            QScrollBar:horizontal {{
                border: none;
                background: transparent;
                height: 10px;
                margin: 0px 4px 2px 4px;
            }}
            QScrollBar::handle:horizontal {{
                background: #c4c4c4;
                border-radius: 5px;
                min-width: 24px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: #a6a6a6;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
        """)

    def _make_checkbox_cell(self, checked=False):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        checkbox = QCheckBox()
        checkbox.setChecked(bool(checked))
        layout.addWidget(checkbox)
        return container

    def _make_actions_cell(self, actions, row_data):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignCenter)
        for label, callback in actions:
            button = QPushButton(label)
            button.setCursor(Qt.PointingHandCursor)
            if callback:
                button.clicked.connect(lambda _checked, r=row_data: callback(r))
            layout.addWidget(button)
        return container

    def add_row(self, row_data: dict):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setRowHeight(row, 44)

        for i, col in enumerate(self.columns):
            key = col.get("key")
            value = row_data.get(key)
            factory = col.get("factory")
            col_type = col.get("type", "widget" if factory else "text")

            if factory is not None:
                self.table.setCellWidget(row, i, factory(value, row_data))

            elif col_type == "checkbox":
                self.table.setCellWidget(row, i, self._make_checkbox_cell(value))

            elif col_type == "actions":
                self.table.setCellWidget(
                    row, i, self._make_actions_cell(col.get("actions", []), row_data)
                )

            else:
                item = QTableWidgetItem("" if value is None else str(value))
                if col.get("center"):
                    item.setTextAlignment(Qt.AlignCenter)
                if col.get("color"):
                    item.setForeground(col["color"])
                self.table.setItem(row, i, item)

    def clear_rows(self):
        self.table.setRowCount(0)

    def populate(self, rows: list):
        self.clear_rows()
        for row_data in rows:
            self.add_row(row_data)

    def get_cell_value(self, row: int, col_index: int):
        widget = self.table.cellWidget(row, col_index)
        if widget is None:
            item = self.table.item(row, col_index)
            return item.text() if item else None

        checkbox = widget.findChild(QCheckBox)
        if checkbox is not None:
            return checkbox.isChecked()

        if isinstance(widget, QComboBox):
            return widget.currentText()

        return None


