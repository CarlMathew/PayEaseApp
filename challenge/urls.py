from django.urls import path
from . import views
urlpatterns = [
    path('main', view = views.home),
    path('scan', view = views.scanRFID),
    path('check', view = views.checkbal),
    path('coins', view = views.coinInsertedData),
    path('totalCoin', view = views.total_coins),
    path("receipt", view = views.print_receipt)
]