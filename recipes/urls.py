from django.urls import path
from .views import RecommendRecipeAPIView

urlpatterns = [
    path('recommend/', RecommendRecipeAPIView.as_view()),
]
