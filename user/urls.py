from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from . import views

app_name = 'user'

urlpatterns = [
    # 로그인/회원가입
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('signup/', views.SingupView.as_view()),
    path('delete/', views.UserDeleteView.as_view()),
    path('password/change/', views.PasswordChangeView.as_view()),
    # 프로필
    path('profile/', views.ProfileView.as_view()),
    # 토큰
    path('token/refresh/', views.RefreshTokenView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]