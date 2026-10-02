import requests
from PyQt5.QtCore import QThread, pyqtSignal

class ApiError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload


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
        """Sends credentials to obtain JWT tokens and user payload."""
        data = self.send("POST", "/api/auth/token/", json={"email": email, "password": password}, auth=False)
        
        self.access = data.get("access")
        self.refresh = data.get("refresh")
        self.user = data.get("user")
        return self.user

    def send(self, method, path, auth=True, **kwargs):
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
                error_msg = data.get("detail") or data.get("non_field_errors") or data.get("error") or error_msg
                if isinstance(error_msg, list):
                    error_msg = error_msg[0]
            elif resp.status_code == 403:
                error_msg = "You do not have permission to do that."

            raise ApiError(error_msg, status_code=resp.status_code, payload=data)

        return data


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
            
            user_data = self.api_client.login(
                self.email,
                self.password
            )

            print("[DEBUG] Login returned:")
            print(user_data)
            print("[DEBUG] Type:", type(user_data))

            self.login_success.emit(user_data or {})

        except Exception as e:
            import traceback

            print("\n========== LOGIN ERROR ==========")
            traceback.print_exc()
            print("=================================\n")

            msg = getattr(e, "message", str(e))
            self.login_failed.emit(msg)
