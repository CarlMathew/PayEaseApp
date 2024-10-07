
# /dev/ttyAMA0
# /dev/ttyUSB0
import serial

# Open the serial port (replace '/dev/ttyUSB1' with the correct port)
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Wait for data
while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip().split(" ")
        print(f"{data}")
        if "Open" in data and "is" in data:
            break

question = input("Already Click? ")
if question == "yes":
    print("Good")

        
