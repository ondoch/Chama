PERMISSIONS = [
    ("create_chama", "Create chama", "Chama management", ["access.create_chama"]),
    ("view_chama_details", "View chama details", "Chama management", ["access.view_chama_details"]),
    ("update_chama_info", "Update chama info", "Chama management", ["access.update_chama_info"]),
    ("configure_chama_settings", "Configure chama settings", "Chama management", ["access.configure_chama_settings"]),

    ("add_members", "Add members", "Member management", ["access.add_members"]),
    ("view_members", "View members", "Member management", ["access.view_members"]),
    ("update_member_information", "Update member information", "Member management", ["access.update_member_information"]),
    ("remove_member", "Remove member", "Member management", ["access.remove_member"]),

    ("view_reports", "View reports", "System access", ["access.view_reports"]),
    ("view_audits", "View audits", "System access", ["access.view_audits"]),
    ("manage_employees", "Manage employees", "System access", ["employee.view_employee", "employee.add_employee", "employee.change_employee", "employee.delete_employee"]),
]

ALL_PERMISSION_KEYS = [p[0] for p in PERMISSIONS]

ROLES = [
    ("chama_facilitator", "Chama Facilitator",
     ["create_chama", "view_chama_details", "update_chama_info"]),
    ("chama_supervisor", "Chama Supervisor",
     ["view_chama_details", "update_chama_info", "configure_chama_settings"]),
    ("finance_support", "Finance Support",
     ["view_chama_details", "view_members", "view_reports"]),
    ("super_admin", "Super Admin",
     ALL_PERMISSION_KEYS),
]

PERMISSION_BY_KEY = {key: {"key": key, "label": label, "group": group, "django": django}
                     for key, label, group, django in PERMISSIONS}

ROLE_BY_KEY = {key: {"key": key, "label": label, "permissions": perms}
               for key, label, perms in ROLES}
