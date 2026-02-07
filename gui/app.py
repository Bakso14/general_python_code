import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGridLayout
from PySide6.QtGui import QPalette, QColor
from layout_colorwidget import Color

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elektronika Industri")

        layout = QGridLayout()
        widget1 = Color("red")
        widget2 = Color("green")
        self.widget3 = QPushButton("Tombol")

        layout.addWidget(widget1, 0,0)
        layout.addWidget(widget2, 1,1)
        layout.addWidget(self.widget3, 2,2)

        widget_total = QWidget()
        widget_total.setLayout(layout)

        self.setCentralWidget(widget_total)

        self.widget3.clicked.connect(self.button_pushed)

    def button_pushed(self):
        print("Tombol ditekan")
        self.widget3.setText("Sudah Ditekan")



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()