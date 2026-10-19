from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)

from widgets.onboarding_dashboard import Onboarding

class OnboardingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = Onboarding()

        layout.addWidget(widget)
