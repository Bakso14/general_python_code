import serial_arduino
import time

# Configure the serial port
ser = serial_arduino.Serial(
    port='/dev/ttyUSB0',  # Replace with your serial port
    baudrate=9600,
    timeout=1
)

# Function to send data
def send_data(data):
    ser.write(data.encode())
    print(f"Sent: {data}")

# Function to read data
def read_data():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        print(f"Received: {data}")
        return data
    return None

# Main loop
try:
    while True:
        # Send data
        send_data('Hello, Device!')
        # Wait for a response
        response = read_data()
        # Pause for a moment
        time.sleep(2)
except KeyboardInterrupt:
    # Close the serial port
    ser.close()
    print("Serial port closed.")