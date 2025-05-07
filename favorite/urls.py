from django.urls import path
from favorite import views

urlpatterns = [
    path('likes/<int:recipe_id>', views.toggle_like, name='toggle_like'),
    path('likes', views.liked_recipes, name='liked_recipes'),
]