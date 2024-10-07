import threading
import time 
from mfrc522 import SimpleMFRC522
from django.core.cache import cache
import RPi.GPIO as GPIO

class RFIDREader(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.rfid = SimpleMFRC522()
    
    def run(self):
        while self.running:
            try:
                id, text = self.rfid.read()
                if id is not None:
                    cache.set('rfid', {'id': id})
            except Exception as e:
                print('Error readinf RFID')
            finally:
                GPIO.cleanup() 
        time.sleep(1)
    
    def stop(self):
        self.running = False
    