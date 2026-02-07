import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PySide6.QtCore import QTimer

import serial

class SerialReader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serial Reader PySide6")

        # Layout
        layout = QVBoxLayout()

        self.label = QLabel("Data Serial:")
        layout.addWidget(self.label)

        self.text_area = QTextEdit()
        layout.addWidget(self.text_area)

        self.btn_start = QPushButton("Mulai Baca")
        self.btn_start.clicked.connect(self.start_reading)
        layout.addWidget(self.btn_start)

        self.setLayout(layout)

        # Variabel serial
        self.ser = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)

    def start_reading(self):
        try:
            self.ser = serial.Serial('COM3', 9600, timeout=1)
            self.timer.start(100)  # baca tiap 100 ms
            self.btn_start.setEnabled(False)
        except Exception as e:
            self.text_area.append(f"Error: {e}")

    def read_serial(self):
        if self.ser and self.ser.in_waiting:
            data = self.ser.readline().decode('utf-8').strip()
            self.text_area.append(data)

    def closeEvent(self, event):
        if self.ser:
            self.ser.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialReader()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
