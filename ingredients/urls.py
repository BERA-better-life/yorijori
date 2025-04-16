from django.urls import path
from .views import UserIngredientsListCreateView, UserIngredientsDeleteView, ExcludedIngredientsListCreateView, ExcludedIngredientsDeleteView

urlpatterns = [
    path('user-ingredients', UserIngredientsListCreateView.as_view(), name='user-ingredients-list-create'),
    path('user-ingredients/<int:user_ingredient_id>', UserIngredientsDeleteView.as_view(), name='user-ingredients-delete'),
    path('ingredients/excluded', ExcludedIngredientsListCreateView.as_view(), name='excluded-ingredients-list-create'),
    path('ingredients/excluded/<int:excluded_id>', ExcludedIngredientsDeleteView.as_view(), name='excluded-ingredients-delete'),
]
