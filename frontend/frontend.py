from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout)
from windows.main_window import MainWindow

class FrontEnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chama Manager")
        self.trialUI()

    def trialUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)

        widget1 = MainWindow()
        main_layout.addWidget(widget1)

        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication([])
    frontend = FrontEnd()
    frontend.show()
    app.exec_()
