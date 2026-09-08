from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout)
from widgets.employee_widget import AddEmployee

class FrontEnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FrontEnd")
        self.trialUI()

    def trialUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        widget1 = AddEmployee()
        main_layout.addWidget(widget1)

        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication([])
    frontend = FrontEnd()
    frontend.show()
    app.exec_()
