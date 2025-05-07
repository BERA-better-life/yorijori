from django.urls import path
from .views import RecipeRecommendAPIView
from .views import RecipeRecommendWithExcludedAPIView

urlpatterns = [
        path('recommend/', RecipeRecommendAPIView.as_view(), name='recipe-recommend'),  # 기존 뷰
        path('recommend/exclude/', RecipeRecommendWithExcludedAPIView.as_view(), name='recipe-recommend-with-exclusion'),  # 기존 뷰
]