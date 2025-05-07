from django.urls import path
from .views import RecipeRecommendAPIView

urlpatterns = [
        path('recommend/', RecipeRecommendAPIView.as_view(), name='recipe-recommend'),  # 기존 뷰

]