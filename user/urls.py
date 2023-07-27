from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

app_name = 'user'

urlpatterns = [
    # 로그인/회원가입
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('signup/', views.SingupView.as_view()),
    # 토큰
    path('token/refresh/', views.RefreshTokenView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]