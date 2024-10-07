from django.shortcuts import render
from django.http import request, JsonResponse
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from .SQLConfig import APPSQL
import json
# Create your views here.

def home(request):
    return render(request, 'challenge/main.html')

def scanRFID(request):
    connection = APPSQL('sql12735044')
    print("accessing")
    reader = SimpleMFRC522()
    print("Working")
    # Ensure that the request method is POST
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            location1,location2 = data.get('loc1'),data.get('loc2')
            
            id, text = reader.read()
            query_loco = f"SELECT * FROM Locations WHERE Location1 = '{location1}' AND Location2 = '{location2}'"
            payment = connection.read_database(query_loco)[0]['Price']
            query1 = f"SELECT * FROM Users WHERE RFID = {id}"
            results = connection.read_database(query1)
            current_balance = results[0]['Balance']
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
    reader = SimpleMFRC522()
    id, text = reader.read()

    if request.method == "POST":
        query_bal = f"SELECT * FROM Users WHERE RFID = {id}"
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
    
