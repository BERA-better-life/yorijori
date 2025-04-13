from django.urls import path
from .views import expiration_alerts_view

urlpatterns = [
    path("api/expiration/alerts/<int:user_id>", expiration_alerts_view),
]
