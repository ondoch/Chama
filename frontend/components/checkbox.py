from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QCheckBox
)

class CheckBox(QFrame):
    def __init__(self, label_text, object_name=None, parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.object_name_ = object_name
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.check_box = QCheckBox(self.label_text)
        if self.object_name_:
            self.check_box.setObjectName(self.object_name_)

        layout.addWidget(self.check_box)

    def returnValue(self):
        return self.check_box.isChecked()
