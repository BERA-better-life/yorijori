# users/urls.py
from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, CheckUsernameView, CheckEmailView, DeleteUserView, LogoutView, UserInfoView, AllUsersView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('check-username', CheckUsernameView.as_view(), name='check-username'),
    path('check-email', CheckEmailView.as_view(), name='check-email'),
    path('me', UserInfoView.as_view(), name='user-info'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('all', AllUsersView.as_view(), name='all-users'),
]