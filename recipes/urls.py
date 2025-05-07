from django.urls import path
from .views import RecipeRecommendAPIView
from .views import RecipeRecommendWithExcludedAPIView
from .views import RecipeDetailAPIView

urlpatterns = [
        path('recommend/', RecipeRecommendAPIView.as_view(), name='recipe-recommend'),  # 기존 뷰
        path('recommend/exclude/', RecipeRecommendWithExcludedAPIView.as_view(), name='recipe-recommend-with-exclusion'), 
        path('recipe/<int:rcp_number>/', RecipeDetailAPIView.as_view(), name='recipe-detail'),
]