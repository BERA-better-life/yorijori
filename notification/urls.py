from django.urls import path
from .views import send_expiration_notifications

urlpatterns = [
    path('notify/', send_expiration_notifications, name='send_expiration_notifications'),
]