from django.apps import AppConfig
from .rfidThread import RFIDREader

class ChallengeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'challenge'

class RFIDAPPConfig(AppConfig):
    name = 'rfid_app'
    def ready(self):
        self.rfid_thread = RFIDREader()
        self.rfid_thread.start()


