import sys
import time
from PyQt5.QtWidgets import QApplication
from windows.log_in import LoginWindow
from windows.main_window import MainWindow

# ---- Development switches -------------------------------------------------
DEV_MODE = False
DEV_SKIP_LOGIN = True
# -----------------------------------------------------------------------------

if DEV_MODE:

    class APIClient:
        DEV_EMAIL = "dev@test.com"
        DEV_PASSWORD = "admin123"

        def login(self, email, password):
            time.sleep(0.8)

            if email == self.DEV_EMAIL and password == self.DEV_PASSWORD:
                return {
                    "email": email,
                    "first_name": "Dev",
                    "last_name": "User",
                    "is_staff": True,
                    "roles": [["administrator"]],
                }

            raise Exception("Invalid email or password.")

        def logout(self):
            pass

else:
    from api.api_client import APIClient


class AppController:

    def __init__(self):
        self.api = APIClient()

        self.login_window = None
        self.main_window = None

    def start(self):

        if DEV_MODE and DEV_SKIP_LOGIN:
            # Fallback dummy data for dev mode
            dev_user = {
                "first_name": "Dev",
                "last_name": "User",
                "roles": [["administrator"]],
            }
            self.show_main(user_data=dev_user)
        else:
            self.show_login()

    def show_login(self):
        self.login_window = LoginWindow(self.api)
        self.login_window.login_successful.connect(self.on_login_successful)
        self.login_window.show()

    def on_login_successful(self, user_data):
        print("[DEBUG] AppController received successful login")
        print("[DEBUG] Logged in user:")
        print(user_data)

        print("[DEBUG] About to open MainWindow...")

        try:
            # FIX: Pass user_data to show_main
            self.show_main(user_data=user_data)
            print("[DEBUG] MainWindow opened successfully")

        except Exception as e:
            import traceback

            print("\n========== MAIN WINDOW ERROR ==========")
            traceback.print_exc()
            print("=======================================\n")

    def show_main(self, user_data=None):

        print("[DEBUG] Entered show_main()")

        print("[DEBUG] Creating MainWindow...")

        self.main_window = MainWindow(self.api, user_data=user_data)

        print("[DEBUG] MainWindow object created")

        self.main_window.setWindowTitle("Chama Manager")

        print("[DEBUG] Connecting logged_out signal...")

        self.main_window.logged_out.connect(self.on_logged_out)

        print("[DEBUG] Showing MainWindow...")

        self.main_window.showMaximized()

        print("[DEBUG] MainWindow is now visible")

        if self.login_window:
            print("[DEBUG] Closing LoginWindow...")

            self.login_window.close()
            self.login_window.deleteLater()
            self.login_window = None

        print("[DEBUG] show_main() completed")

    def on_logged_out(self):

        if self.main_window:
            self.main_window.close()
            self.main_window.deleteLater()
            self.main_window = None

        self.show_login()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = AppController()
    controller.start()
    sys.exit(app.exec_())