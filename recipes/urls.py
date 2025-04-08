from django.urls import path
from .views import RecipeRecommendationView  # 기존 views에서 가져오는 부분
from .views_ver2 import RecipeRecommendationView as RecipeRecommendationViewVer2  # views_ver2에서 가져오기

urlpatterns = [
    path('recommend/', RecipeRecommendationView.as_view(), name='recipe-recommend'),  # 기존 뷰
    path('recommend_v2/', RecipeRecommendationViewVer2.as_view(), name='recipe-recommend-v2'),  # 새로운 뷰
]