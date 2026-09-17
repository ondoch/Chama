from PyQt5.QtWidgets import QFrame, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class ContextMenu(QFrame):
    def __init__(self, parent=None, row_data=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.row_data = row_data
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(2)

        add_member = QPushButton("Add member")
        add_member.clicked.connect(self._on_add_member)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        set_officials = QPushButton("Set officials")
        set_officials.clicked.connect(self._on_set_officials)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)

        delete = QPushButton("Delete")
        delete.clicked.connect(self._on_delete)

        main_layout.addWidget(add_member)
        main_layout.addWidget(line)
        main_layout.addWidget(set_officials)
        main_layout.addWidget(line2)
        main_layout.addWidget(delete)

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }

            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 10px 14px;
                text-align: left;
                font-size: 14px;
                color: #374151;
            }

            QPushButton:hover {
                background-color: #F3F4F6;
                color: #111827;
            }

            QPushButton:pressed {
                background-color: #E5E7EB;
            }

            QFrame[frameShape="4"] {
                color: #E5E7EB;
                max-height: 1px;
            }
        """)
        self.setFixedWidth(180)

    def _on_add_member(self):
        self.close()
        parent = self.parent()
        if parent is not None and hasattr(parent, "openAddMemberDialog"):
            parent.openAddMemberDialog(self.row_data)

    def _on_set_officials(self):
        self.close()
        parent = self.parent()
        if parent is not None and hasattr(parent, "openOfficialsDialog"):
            parent.openOfficialsDialog(self.row_data)
        else:
            print("Set officials for", self.row_data)

    def _on_delete(self):
        self.close()
        parent = self.parent()
        if parent is not None and hasattr(parent, "openDeleteDialog"):
            parent.openDeleteDialog(self.row_data)

    @staticmethod
    def show_at_button(button, parent=None, row_data=None):
        menu = ContextMenu(parent=parent, row_data=row_data)
        if button is not None:
            pos = button.mapToGlobal(button.rect().bottomRight())
            menu.move(pos.x() - menu.sizeHint().width(), pos.y())
        else:
            menu.move(QCursor.pos())
        menu.show()
        return menu