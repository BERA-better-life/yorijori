from django.urls import path
from favorite import views

urlpatterns = [
    path('likes/<int:recipe_id>', views.toggle_like, name='toggle_like'),
    path('likes', views.liked_recipes, name='liked_recipes'),
    path('bookmarks/<int:recipe_id>', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks', views.bookmarked_recipes, name='bookmarked_recipes'),
]