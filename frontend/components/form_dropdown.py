from PyQt5.QtWidgets import (
    QComboBox
)

class FormDropdown(QComboBox):
    def __init__(self, placeholder, items=None, height=None, icon_path="resources/down_arrow.svg"):
        super().__init__()
        self.setObjectName("formDropdown")

        self.height = height

        self.setFixedHeight(int(self.height))
        self.setEditable(False)

        if placeholder:
            self.addItem(placeholder)
            self.model().item(0).setEnabled(False)
        self.addItems(items or [])
        self.setCurrentIndex(0)

        icon_path = icon_path.replace("\\", "/")

        self.setStyleSheet(f"""
            QComboBox#formDropdown {{
                border: 1px solid #D8DBDE;
                border-radius: 5px;
                padding: 0 12px;
                font-size: 12px;
                font-family: Arial, sans-serif;
                background-color: white;
                color: #333333;
            }}
            QComboBox#formDropdown:hover {{
                border: 1px solid #B7BBC0;
            }}
            QComboBox#formDropdown:focus {{
                border: 1px solid #4A90D9;
            }}
            QComboBox#formDropdown::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 30px;
                border: none;
            }}
            QComboBox#formDropdown::down-arrow {{
                image: url({icon_path});
                width: 12px;
                height: 12px;
                margin-right: 10px;
            }}
            QComboBox#formDropdown QAbstractItemView {{
                border: 1px solid #D8DBDE;
                border-radius: 5px;
                background-color: white;
                selection-background-color: #F0F2F4;
                selection-color: #333333;
                outline: none;
                padding: 4px;
            }}
            QComboBox#formDropdown QAbstractItemView::item {{
                min-height: 28px;
                padding-left: 8px;
            }}
        """)

    def returnValue(self):
        if self.currentIndex() <= 0:
            return None
        return self.currentText()