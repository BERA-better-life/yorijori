from django.urls import path
from .views import recommend_ingredients

urlpatterns = [
    path('recommend-ingredients', recommend_ingredients),
]
