import serial
import time

# Use the identified port for the Arduino
ser = serial.Serial('/dev/ttyACM1', 9600)

# Example: Reading data from the Arduino
try:
    while True:
        raw_data = ser.readline()  # Read raw bytes
        try:
            data = raw_data.decode('utf-8').strip()  # Try decoding to UTF-8
            print(data)  # Process your decoded data here
            with open("/home/pi/Desktop/PayEaseAPP/payEase/challenge/static/challenge/coinSlot.txt", "w") as f:
                f.write(data)

        except UnicodeDecodeError:
            print(f"Received non-UTF-8 data: {raw_data}")  # Print raw data for debugging
except serial.SerialException as e:
    print(f"Serial exception: {e}")
finally:
    ser.close()  # Close the serial port when done
