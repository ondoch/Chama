from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal

from api.api_client import LoginWorker
from api.api_client import APIClient

from components.member_form_input import MemberFormInput
from components.password_form_input import PasswordFormInput
from components.banner import Banner
from components.style_constants import (
    COLOR_CARD_BG,
    COLOR_BORDER,
    COLOR_ACCENT_BLUE
)

CARD_WIDTH = 380

class LoginWindow(QMainWindow):
    login_successful = pyqtSignal(dict)

    def __init__(self, api_client = None):
        super().__init__()
        self.api_client = api_client or APIClient()
        self.login_worker = None

        self.setWindowTitle("Chama Manager - Log In")
        self.setFixedSize(560, 520)
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setAlignment(Qt.AlignCenter)

        container = QWidget()
        container.setObjectName("container")
        container.setFixedWidth(CARD_WIDTH)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(7,0,7,15)
        container_layout.setSpacing(10)

        banner = Banner("resources/lock.svg", "Log In", "Log in to the system")
        container_layout.addWidget(banner, alignment=Qt.AlignLeft)

        self.email_address = MemberFormInput("Email Address")
        self.password = PasswordFormInput("Password", "resources/eye_on.svg", "resources/eye_off.svg")

        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        self.error_label.setWordWrap(True)
        self.error_label.hide()

        self.login_btn = QPushButton("Log In")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setFixedHeight(42)
        self.login_btn.clicked.connect(self.handle_login)

        self.password.entry.returnPressed.connect(self.handle_login)

        container_layout.addWidget(self.email_address)
        container_layout.addWidget(self.password)
        container_layout.addWidget(self.error_label)
        container_layout.addSpacing(4)
        container_layout.addWidget(self.login_btn)

        main_layout.addWidget(container)

    def handle_login(self):
        if not self.login_btn.isEnabled():
            return

        email_empty = self.email_address.isEmpty()
        password_empty = self.password.isEmpty()

        self.email_address.setError(email_empty)
        self.password.setError(password_empty)

        if email_empty or password_empty:
            self.show_error(
                "Please enter your email address and password."
            )
            return

        self.error_label.hide()

        email = self.email_address.returnValue()
        password = self.password.returnValue()

        self.set_busy(True)

        self.login_worker = LoginWorker(
            self.api_client,
            email,
            password
        )

        self.login_worker.login_success.connect(
            self.on_login_success
        )

        self.login_worker.login_failed.connect(
            self.on_login_failed
        )

        self.login_worker.start()

    def on_login_success(self, user_data):
        print("[DEBUG] on_login_success called")
        print("[DEBUG] user_data:", user_data)

        self.set_busy(False)

        print("[DEBUG] Emitting login_successful")

        self.login_successful.emit(user_data)

        print("[DEBUG] login_successful emitted successfully")

    def on_login_failed(self, error_msg):
        self.set_busy(False)
        self.show_error(error_msg)

    def set_busy(self, busy):
        self.login_btn.setEnabled(not busy)
        self.login_btn.setText("Logging in..." if busy else "Log In")
        self.email_address.setEnabled(not busy)
        self.password.setEnabled(not busy)

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#central{{
                background-color: #F4F6F8;
            }}
            QWidget#container{{
                background-color: {COLOR_CARD_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 10px;
            }}
            QLabel#error{{
                color: #E53935;
                font-size: 12px;
                font-family: Arial, sans-serif;
            }}
            QPushButton#loginBtn{{
                background-color: {COLOR_ACCENT_BLUE};
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                font-family: Arial, sans-serif;
                margin-left: 10px;
                margin-right: 10px;
            }}
            QPushButton#loginBtn:hover{{
                background-color: #1E5FD1;
            }}
            QPushButton#loginBtn:pressed{{
                background-color: #1A4FAE;
            }}
            QPushButton#loginBtn:disabled{{
                background-color: #9DB7E8;
            }}
        """)
