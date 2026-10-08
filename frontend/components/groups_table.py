from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal

from components.custom_table import CustomTable
from components.avatar import Avatar
from components.action_buttons import ActionButtonGroup
from components.context_menu import ContextMenu
from components.style_constants import FONT_FAMILY, COLOR_TEXT_PRIMARY
from tabs.chama.tab_3 import Tab3
from modals.members_information import MemberInformation
from modals.member_summary import MemberSummaryDialog


def _make_avatar_cell(value, row_data):
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(8, 0, 0, 0)
    layout.setSpacing(8)
    layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

    layout.addWidget(Avatar(text=value))

    name_label = QLabel(value or "")
    name_label.setStyleSheet(
        f"font-family: {FONT_FAMILY}; color: {COLOR_TEXT_PRIMARY}; font-size: 14px;"
    )
    layout.addWidget(name_label)
    layout.addStretch()
    return container


def _actions_factory(actions_config):
    def factory(value, row_data):
        return ActionButtonGroup(actions_config, row_data=row_data)
    return factory


class GroupsTable(CustomTable):
    edit_requested = pyqtSignal(dict)
    close_requested = pyqtSignal(dict)
    add_member_requested = pyqtSignal(dict, dict)
    officials_saved = pyqtSignal(dict)

    def __init__(self, api_client=None):
        self.api_client = api_client

        columns = [
            {"header": "Group name", "key": "name", "factory": _make_avatar_cell},
            {"header": "Members", "key": "member_count", "center":True},
            {"header": "Contribution", "key": "contribution", "center":True},
            {"header": "Created on", "key": "created_on", "center":True},
            {"header": "Actions", "key": None, "width": 110,
             "factory": _actions_factory([
                 {"label": "View", "width": 60,
                  "callback": lambda row, btn=None: self.openMemberSummaryDialog(row)},
                 {"icon": "resources/more-vertical.svg",
                  "callback": lambda row, btn=None: self.openContextMenu(row, btn)},
             ])},
        ]
        super().__init__(columns)

    def openContextMenu(self, row, button=None):
        ContextMenu.show_at_button(button, parent=self, row_data=row)

    def openEditDialog(self, row):
        if row:
            self.edit_requested.emit(row)

    def openAddMemberDialog(self, row):
        if not row:
            return
        dialog = MemberInformation(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.add_member_requested.emit(row, dialog.values)

    def openMemberSummaryDialog(self, row):
        dialog = MemberSummaryDialog(
            self.api_client,
            row["public_id"],
            chama_name=row.get("name", ""),
            parent=self,
        )
        dialog.exec_()

    def openOfficialsDialog(self, row):
        if not row:
            return
        if self.api_client is None:
            QMessageBox.warning(self, "Set officials", "The API client is not available.")
            return
        if not row.get("public_id"):
            QMessageBox.warning(
                self, "Set officials",
                "This group has no public id, so its officials can't be loaded."
            )
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Set officials")
 
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)

        tab3 = Tab3(self.api_client)
        layout.addWidget(tab3)

        tab3.cancel_clicked.connect(dialog.reject)
        tab3.finish_clicked.connect(dialog.accept)

        tab3.load_chama(row)

        if dialog.exec_() == QDialog.Accepted:
            self.officials_saved.emit(row)

    def openDeleteDialog(self, row):
        name = row.get("name", "this group") if row else "this group"

        confirm = QMessageBox(self)
        confirm.setIcon(QMessageBox.Warning)
        confirm.setWindowTitle("Close group")
        confirm.setText(f'Close "{name}"?')
        confirm.setInformativeText("A closed group can no longer be edited or reopened.")
        confirm.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        confirm.setDefaultButton(QMessageBox.Cancel)

        if confirm.exec_() == QMessageBox.Yes:
            self.close_requested.emit(row)
