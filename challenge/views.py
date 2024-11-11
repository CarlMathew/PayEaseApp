from django.shortcuts import render
from django.http import request, JsonResponse
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from .SQLConfig import APPSQL
import json
import serial
import time
import os
# Create your views here.

def home(request):
    return render(request, 'challenge/main.html')

def scanRFID(request):
    connection = APPSQL('sql12735044')
    print(os.path.exists('/dev/ttyACM0'))
    # Ensure that the request method is POST
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            location1,location2 = data.get('loc1'),data.get('loc2')
            ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
            ser.flush()
            id = ""
            while True:
                if ser.in_waiting > 0:
                    rfid_id = ser.readline().decode('utf-8').strip()
                    if rfid_id != "":
                        id = rfid_id
                        print(id)
                        ser.close()
                        break
            # id, text = reader.read()
            print(id)

            query_loco = f"SELECT * FROM Locations WHERE Location1 = '{location1}' AND Location2 = '{location2}'"
            payment = connection.read_database(query_loco)[0]['Price']
            query1 = f"SELECT * FROM Users WHERE RFID = '{id}'"
            results = connection.read_database(query1)
            current_balance = results[0]['Balance']
   
            if os.path.exists('/dev/ttyACM0'):
                arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
                duration = 4
                start_time = time.time()

                while True:
                    print("running")
                    message = f"{payment}"
                    arduino.write(message.encode("utf-8"))
                    time.sleep(3)   
                    print("Done Sending")

                    if time.time() - start_time > duration:
                        break
                arduino.close()
            else:
                print("Not Connected")


            print(results)
            if len(results) == 0:
                return JsonResponse({
                    'data':2
                })

            elif current_balance >= payment:
                new_balance = current_balance-payment
                update_query = f'UPDATE Users SET Balance = {new_balance} WHERE RFID = "{id}" '
                connection.update_database(update_query)
                return JsonResponse({
                    'data': 0,
                    'total_payment': payment,
                    'new_bal': new_balance
                })
            elif current_balance < payment:
                return JsonResponse({
                    'data':1 
                })
        except IndexError as e:
            return JsonResponse({'data': 2})
            
        except Exception as e:
            response_data = {"error": str(e)}
            return JsonResponse(response_data)
        finally:
            GPIO.cleanup()  # Clean up GPIO resources
            connection.connection.close()
    return JsonResponse({"error": "Invalid request method"}, status=400)

def checkbal(request):
    print('running check bal')
    connection = APPSQL('sql12735044')
    # reader = SimpleMFRC522()
    # id, text = reader.read()


    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    id = ""
    while True:
        if ser.in_waiting > 0:
            rfid_id = ser.readline().decode('utf-8').strip()
            if rfid_id != "":
                id = rfid_id
                print(id)
                ser.close()
                break
    if request.method == "POST":
        query_bal = f"SELECT * FROM Users WHERE RFID = '{id}'"
        results = connection.read_database(query_bal)
        if len(results) == 0:
            GPIO.cleanup()  # Clean up GPIO resources
            connection.connection.close()

            return JsonResponse({'data': 0})
        else:
            current_bal = results[0]['Balance']
            GPIO.cleanup()  # Clean up GPIO resources
            connection.connection.close()
            return JsonResponse({'data': 1, 'current_bal': current_bal})
        
def coinInsertedData(request):
    if request.method == "POST":
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        connection = APPSQL('sql12735044')
        data = json.loads(request.body)
        location1,location2, totalCoin = data.get('loc1'),data.get('loc2'), data.get("coin")
        query_loco = f"SELECT * FROM Locations WHERE Location1 = '{location1}' AND Location2 = '{location2}'"
        payment = connection.read_database(query_loco)[0]['Price']
        print(location1, location2, totalCoin)
        # try:
        #     while True:
        #         total_coin = 0
        #         raw_data = ser.readline()  # Read raw bytes
        #         try:
        #             data = raw_data.decode('utf-8').strip()  # Try decoding to UTF-8
        #             coin = int(data)
        #             print(coin)
        #             if total_coin != coin:
        #                 total_coin += coin
        #                 query_coin = f"UPDATE Coin SET Coins = {total_coin} WHERE ID = 1"
        #                 print("Running")
        #                 connection.update_database(query_coin)
        #             if coin >= payment:
        #                 break
        #                 connection.connection.close()

        #         except UnicodeDecodeError:
        #             print(f"Received non-UTF-8 data: {raw_data}")  # Print raw data for debugging
        # except serial.SerialException as e:
        #     print(f"Serial exception: {e}")


        # data = json.loads(request.body)
        # location1,location2 = data.get('loc1'),data.get('loc2')
        # query_loco = f"SELECT * FROM Locations WHERE Location1 = '{location1}' AND Location2 = '{location2}'"
        # payment = connection.read_database(query_loco)[0]['Price']
        # ser = serial.Serial('/dev/ttyUSB0', 9600)
        # while True :
        #     if ser.in_waiting > 0:
        #         total_coin = 0
        #         raw_data = ser.readline()  # Read raw bytes
        #         data = raw_data.decode('utf-8').strip()  # Try decoding to UTF-8
        #         print(int(data))  # Process your decoded data here
        #         # coin = int(data)
        #         # if total_coin != coin:
        #         #     total_coin = coin
        #         #     query_coin = f"UPDATE Coin SET Coins = {total_coin} WHERE ID = 1"
        #         #     connection.update_database(query_coin)
        #         #     print(f"total_coin: {total_coin}; coin: {coin}")
        #         # if coin >= payment:
        #         #     break
        #         #     connection.connection.close()
        
        return JsonResponse({"status": True})
        
def total_coins(request):
    if request.method == "GET":
        with open("/home/pi/Desktop/PayEaseAPP/payEase/challenge/static/challenge/coinSlot.txt") as f:
            file = f.read()
            print(file)

        # ser = serial.Serial('/dev/ttyUSB0', 9600)
        # raw_data = ser.readline()
        # data = raw_data.decode('utf-8').strip()
        # print(data)
        return JsonResponse({"data":file})

def print_receipt(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment = data.get("payment")
        arduino = serial.Serial('/dev/ttyACM1', 9600, timeout = 1)
        duration = 4
        start_time = time.time()
        try:
            while True:
                message = f"{payment}"
                arduino.write(message.encode("utf-8"))
                time.sleep(3)   
                print("Done Sending")

                if time.time() - start_time > duration:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            arduino.close()
            return JsonResponse({"Status": "Hatdog"})





        
        