import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("My App")
        self.pushButton.clicked.connect(self.on_button_clicked)    
        self.pushButton_2.clicked.connect(self.on_button2_clicked)

    def on_button_clicked(self):
        print("Button clicked!")

    def on_button2_clicked(self):
        self.setWindowTitle("Button 2 clicked!")

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()