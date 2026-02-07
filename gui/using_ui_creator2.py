import sys
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

loader = QUiLoader()

def mainwindow_setup(w):
    w.setWindowTitle("Using UI Creator 2")
    button = w.findChild(QtWidgets.QPushButton, "pushButton")
    button2 = w.findChild(QtWidgets.QPushButton, "pushButton_2")
    button.clicked.connect(on_button_clicked)
    button2.clicked.connect(on_button2_clicked)

def on_button_clicked():
    print("Button clicked!")

def on_button2_clicked(w):
    window.setWindowTitle("Button 2 clicked!")

app = QtWidgets.QApplication(sys.argv)
window = loader.load("mainwindow.ui", None)
mainwindow_setup(window)
window.show()
app.exec()