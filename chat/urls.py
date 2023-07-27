from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('list/', views.ChatList.as_view()),
    path('list/self/', views.UserChatList.as_view()),
    path('detail/<int:chat_id>', views.ChatDetail.as_view()),
    path('<int:chat_id>/update', views.ChatUpdate.as_view()),
    path('write/', views.ChatWrite.as_view()),
    # path('register/', views.Registration.as_view(), name='register'),
    # path('login/', views.Login.as_view(), name='login'),
    # path('logout/', views.Logout.as_view(), name='logout'),
    # path('profile/write', views.ProfileWrite.as_view(), name="pf-write"),
    # path('profile/delete', views.ProfileDelete.as_view(), name="pf-delete"),
    # path('profile/update', views.ProfileUpdate.as_view(), name="pf-update"),
]