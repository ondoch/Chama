from components.custom_table import CustomTable
from components.action_buttons import ActionButtonGroup


def actions_factory(actions_config):
    def factory(value, row_data):
        return ActionButtonGroup(actions_config, row_data=row_data)
    return factory


def build_columns(on_view=None):
    def view_clicked(row, btn=None):
        if on_view:
            on_view(row)
        else:
            print("View", row)

    return [
        {"header": "Actor", "key": "actor"},
        {"header": "Action", "key": "action"},
        {"header": "Target", "key": "target_label"},
        {"header": "Created at", "key": "created_at"},
        {"header": "Actions", "key": None, "width": 110,
         "factory": actions_factory([
             {"label": "View", "width": 60, "callback": view_clicked},
         ])},
    ]


class AuditLogTable(CustomTable):
    def __init__(self, on_view=None):
        super().__init__(build_columns(on_view))
