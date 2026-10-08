import requests
from PyQt5.QtCore import QThread, pyqtSignal

class ApiError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class AuthExpired(ApiError):
    """Raised when the refresh token is expired or invalid."""

def _flatten_errors(data, prefix=""):
    lines = []
    if isinstance(data, dict):
        for key, val in data.items():
            name = prefix if str(key).isdigit() else str(key).replace("_", " ").title()
            lines.extend(_flatten_errors(val, name))
    elif isinstance(data, (list, tuple)):
        for item in data:
            lines.extend(_flatten_errors(item, prefix))
    else:
        lines.append(f"{prefix}: {data}" if prefix else str(data))
    return lines

class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000", timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.access = None
        self.refresh = None
        self.user = None

    def check_connection(self):
        url = f"{self.base_url}/api/"
        try:
            response = requests.get(url, timeout=self.timeout)
            print(f"[DEBUG] Checking URL: {url} | Status Code: {response.status_code}")

            if response.status_code == 200:
                return True, "Backend connected successfully"
            else:
                return False, f"Server responded with HTTP {response.status_code} at {url}"

        except requests.exceptions.ConnectionError:
            return False, f"Connection Refused: Is Django running on {self.base_url}?"
        except requests.exceptions.Timeout:
            return False, f"Timed out connecting to {url}"
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}"

    def login(self, email, password):
        data = self.send(
            "POST", "/api/auth/token/",
            json={"email": email, "password": password},
            auth=False,
        )

        if isinstance(data, dict):
            tokens = data.get("tokens", {})
            self.access = data.get("access") or tokens.get("access")
            self.refresh = data.get("refresh") or tokens.get("refresh")
            self.user = data.get("user") or data

        print(f"[DEBUG APIClient] Access Token Set: {bool(self.access)}")
        print(f"[DEBUG APIClient] Refresh Token Set: {bool(self.refresh)}")

        return self.user

    def logout(self):
        self.access = None
        self.refresh = None
        self.user = None

    # ---------------------------------------------------------------- employees
    def list_employees(self, page=1, search="", status=""):
        params = {}
        if page:
            params["page"] = page
        if search:
            params["search"] = search
        if status and status.lower() != "all":
            params["status"] = status
        return self.request("GET", "/api/employees/", params=params)

    def create_employee(self, payload):
        return self.request("POST", "/api/employees/", json=payload)

    def update_employee(self, employee_id, payload):
        return self.request("PUT", f"/api/employees/{employee_id}/", json=payload)

    def get_employee(self, employee_id):
        return self.request("GET", f"/api/employees/{employee_id}/")

    def delete_employee(self, employee_id):
        return self.request("DELETE", f"/api/employees/{employee_id}/")

    # ------------------------------------------------------------------- chamas
    def list_chamas(self, page=1, search="", status="", unassigned=False, assigned_to=None):
        """
        unassigned=True   -> only chamas with no open assignment
        assigned_to=<id>  -> only chamas currently assigned to that employee
        page=None         -> do not send a page parameter
        """
        params = {}
        if page:
            params["page"] = page
        if search:
            params["search"] = search
        if status and status.lower() != "all":
            params["status"] = status.lower()
        if unassigned:
            params["unassigned"] = "true"
        if assigned_to:
            params["assigned_to"] = assigned_to
        return self.request("GET", "/api/chamas/", params=params)

    def create_chama(self, payload):
        return self.request("POST", "/api/chamas/", json=payload)

    def update_chama(self, public_id, payload):
        return self.request("PATCH", f"/api/chamas/{public_id}/", json=payload)

    def set_chama_status(self, public_id, status, reason=""):
        return self.request(
            "POST",
            f"/api/chamas/{public_id}/set-status/",
            json={"status": str(status).lower(), "reason": reason},
        )

    def chama_stats(self):
        return self.request("GET", "/api/chamas/stats/")

    def assign_chama(self, public_id, employee_id):
        return self.request(
            "POST", f"/api/chamas/{public_id}/assign/",
            json={"employee": employee_id},
        )

    def unassign_chama(self, public_id, employee_id):
        return self.request(
            "POST", f"/api/chamas/{public_id}/unassign/",
            json={"employee": employee_id},
        )

    def list_assignments(self, public_id, include_past=False):
        params = {"include_past": "true"} if include_past else {}
        return self.request("GET", f"/api/chamas/{public_id}/assignments/", params=params)

    # ------------------------------------------------------------------ members
    def list_members(self, chama_id, include_removed=False):
        params = {"include_removed": "true"} if include_removed else {}
        return self.request("GET", f"/api/chamas/{chama_id}/members/", params=params)

    def create_member(self, chama_id, payload):
        return self.request("POST", f"/api/chamas/{chama_id}/members/", json=payload)

    # --------------------------------------------------------------- http layer
    def request(self, method, path, **kwargs):
        """Wrapper around send() that handles automatic 401 token refresh."""
        try:
            return self.send(method, path, **kwargs)
        except ApiError as e:
            if e.status_code != 401 or not self.refresh:
                raise

        self.do_refresh()
        return self.send(method, path, **kwargs)

    def do_refresh(self):
        """Refreshes access token using stored refresh token."""
        try:
            data = self.send(
                "POST",
                "/api/auth/token/refresh/",
                json={"refresh": self.refresh},
                auth=False
            )
        except ApiError as e:
            self.logout()
            raise AuthExpired(
                "Your session has expired. Please login again.",
                e.status_code
            ) from e

        self.access = data["access"]
        self.refresh = data.get("refresh", self.refresh)

    def send(self, method, path, auth=True, **kwargs):
        """Executes raw HTTP requests and standardizes responses/errors."""
        headers = kwargs.pop("headers", {})
        if auth and self.access:
            headers["Authorization"] = f"Bearer {self.access}"

        url = f"{self.base_url}{path}"

        try:
            resp = requests.request(method, url, headers=headers, timeout=self.timeout, **kwargs)
        except requests.exceptions.RequestException as e:
            raise ApiError(f"Cannot reach the server at {self.base_url}.") from e

        if resp.status_code == 204:
            return None

        try:
            data = resp.json()
        except ValueError:
            data = None

        if not resp.ok:
            error_msg = "An error occurred."
            if isinstance(data, dict):
                error_msg = data.get("detail") or data.get("non_field_errors") or data.get("error")
                if not error_msg:
                    error_msg = "\n".join(_flatten_errors(data)) or "An error occurred."
                elif isinstance(error_msg, list):
                    error_msg = error_msg[0]
            elif resp.status_code == 403:
                error_msg = "You do not have permission to perform this action."

            raise ApiError(error_msg, status_code=resp.status_code, payload=data)

        return data

    def list_officials(self, chama_id):
        return self.request("GET", f"/api/chamas/{chama_id}/officials/")

    def save_officials(self, chama_id, selection):
        return self.request(
            "PUT", f"/api/chamas/{chama_id}/officials/set/",
            json={"officials": selection},
        )

    @staticmethod
    def _results(data):
        if isinstance(data, dict):
            return data.get("results", [])
        return data or []

    @staticmethod
    def _member_id(official):
        m = official.get("member")
        return m.get("id") if isinstance(m, dict) else m


class ApiWorker(QThread):
    """Runs any callable off the UI thread. Emits its return value or an error message."""
    success = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.success.emit(self.fn(*self.args, **self.kwargs))
        except Exception as e:
            self.error.emit(getattr(e, "message", str(e)))


class ConnectionCheckerWorker(QThread):
    connection_result = pyqtSignal(bool, str)

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client

    def run(self):
        is_connected, message = self.api_client.check_connection()
        self.connection_result.emit(is_connected, message)


class LoginWorker(QThread):
    login_success = pyqtSignal(dict)
    login_failed = pyqtSignal(str)

    def __init__(self, api_client, email, password):
        super().__init__()
        self.api_client = api_client
        self.email = email
        self.password = password

    def run(self):
        try:
            print("[DEBUG] LoginWorker started")
            user_data = self.api_client.login(self.email, self.password)
            self.login_success.emit(user_data or {})
        except Exception as e:
            msg = getattr(e, "message", str(e))
            self.login_failed.emit(msg)


class FetchEmployeesWorker(QThread):
    success = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, api_client, page=1, search="", status=""):
        super().__init__()
        self.api_client = api_client
        self.page = page
        self.search = search
        self.status = status

    def run(self):
        try:
            response = self.api_client.list_employees(
                page=self.page, search=self.search, status=self.status
            )

            if isinstance(response, dict) and "results" in response:
                employees_data = response.get("results", [])
            elif isinstance(response, list):
                employees_data = response
            else:
                employees_data = []

            normalized = []
            for emp in employees_data:
                first = emp.get("first_name", "")
                last = emp.get("last_name", "")
                full_name = f"{first} {last}".strip() or emp.get("email", "Unknown")

                roles = emp.get("roles") or []
                role_str = (
                    ", ".join(r.replace("_", " ").title() for r in roles)
                    or emp.get("job_title")
                    or "Employee"
                )

                raw_status = emp.get("status", True)
                if isinstance(raw_status, bool):
                    status_label = "Active" if raw_status else "Inactive"
                else:
                    status_label = str(raw_status).title()

                normalized.append({
                    "id": emp.get("id"),
                    "name": full_name,
                    "first_name": first,
                    "last_name": last,
                    "email": emp.get("email", ""),
                    "phone": emp.get("phone_number", ""),
                    "role": role_str,
                    "chamas_managed": emp.get("chamas_managed_count", 0),
                    "status": status_label,
                    "raw_data": emp,
                })

            self.success.emit(normalized)

        except Exception as e:
            msg = getattr(e, "message", str(e))
            self.error.emit(msg)

class CreateEmployeeWorker(QThread):
    success = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, api_client, payload):
        super().__init__()
        self.api_client = api_client
        self.payload = payload

    def run(self):
        try:
            result = self.api_client.create_employee(self.payload)
            self.success.emit(result or {})
        except Exception as e:
            msg = getattr(e, "message", str(e))
            self.error.emit(msg)

class UpdateEmployeeWorker(QThread):
    success = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, api_client, employee_id, payload):
        super().__init__()
        self.api_client = api_client
        self.employee_id = employee_id
        self.payload = payload

    def run(self):
        try:
            result = self.api_client.update_employee(self.employee_id, self.payload)
            self.success.emit(result or {})
        except Exception as e:
            msg = getattr(e, "message", str(e))
            self.error.emit(msg)
