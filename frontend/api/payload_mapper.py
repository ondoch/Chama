
import re
from datetime import datetime

PERSONAL = "Personal Information"
ACCESS = "Roles and Permissions"
ROLES_BLOCK = "Roles & Permissions"


def slug(label):
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def _date_to_iso(text):
    try:
        return datetime.strptime(text.strip(), "%d/%m/%Y").date().isoformat()
    except (ValueError, AttributeError):
        return text


def form_to_api(form):
    personal = form[PERSONAL]
    access = form.get(ACCESS, {})

    body = {
        "first_name": personal["first name"].strip(),
        "last_name": personal["last name"].strip(),
        "email": personal["email address"].strip(),
        "national_id": personal["national id"].strip(),
        "phone": personal["phone number"].strip(),
        "job_title": personal["job title"].strip(),
        "date_hired": _date_to_iso(personal["employment date"]),
        "status": personal["status"],             # 'Active', 'On leave', 'Terminated' are all accepted
        "roles": [slug(label) for label, on in access.get(ROLES_BLOCK, {}).items() if on],
        "permissions": [
            slug(label)
            for group, items in access.items() if group != ROLES_BLOCK
            for label, on in items.items() if on
        ],
    }
    employee_id = personal.get("employee ID", "").strip()
    if employee_id:
        body["employee_number"] = employee_id      # optional: the server generates one if omitted
    return body


def api_to_form(employee, catalog):
    held_roles = set(employee.get("roles", []))
    held_perms = set(employee.get("permissions", []))

    access = {ROLES_BLOCK: {r["label"]: r["key"] in held_roles for r in catalog["roles"]}}
    for p in catalog["permissions"]:
        access.setdefault(p["group"], {})[p["label"]] = p["key"] in held_perms

    date_hired = employee.get("date_hired", "")
    try:
        date_hired = datetime.strptime(date_hired, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        pass

    return {
        PERSONAL: {
            "first name": employee.get("first_name", ""),
            "last name": employee.get("last_name", ""),
            "email address": employee.get("email", ""),
            "national id": employee.get("national_id", ""),   # absent if you may not see it
            "job title": employee.get("job_title", ""),
            "phone number": employee.get("phone", ""),
            "employee ID": employee.get("employee_number", ""),
            "employment date": date_hired,
            "status": employee.get("status_display", ""),
        },
        ACCESS: access,
    }
