from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QWidget,
    QCheckBox
)

class CheckBox(QFrame):
    def __init__(self, label_text, object_name=None, parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.object_name_ = object_name
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        container_widget = QWidget()
        container_widget.setObjectName("container")
        container_widget_layout = QHBoxLayout(container_widget)
        container_widget_layout.setContentsMargins(0,0,0,0)

        self.check_box = QCheckBox(self.label_text)
        if self.object_name_:
            self.check_box.setObjectName(self.object_name_)
        container_widget_layout.addWidget(self.check_box)

        main_layout.addWidget(container_widget)
        self.setLayout(main_layout)

    def isChecked(self):
        return self.check_box.isChecked()

    def setChecked(self, checked: bool):
        self.check_box.setChecked(checked)
