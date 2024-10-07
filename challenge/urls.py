from django.urls import path
from . import views
urlpatterns = [
    path('main', view = views.home),
    path('scan', view = views.scanRFID),
    path('check', view = views.checkbal)
]