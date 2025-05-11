from django.urls import path
from .views import UserIngredientsView, ExcludedIngredientsView, expiring_soon_ingredients, AllIngredientsListView

urlpatterns = [
    path('user-ingredients', UserIngredientsView.as_view(), name='user-ingredients'),
    path('excluded', ExcludedIngredientsView.as_view(), name='excluded-ingredients'),
    path('expiring-soon', expiring_soon_ingredients, name='expiring_soon_ingredients'), #notifications
    path('all', AllIngredientsListView.as_view(), name='all-ingredients'),
]
