from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('list/', views.ChatList.as_view()),
    path('list/self/', views.UserChatList.as_view()),
    path('detail/<int:chat_id>/', views.ChatDetail.as_view()),
    path('<int:chat_id>/update/', views.ChatUpdate.as_view()),
    path('write/', views.ChatWrite.as_view()),
    path('delete/<int:chat_id>/', views.ChatDelete.as_view()),
    path('<int:chat_id>/comment/write/', views.CommentWrite.as_view()),
    path('comment/delete/child/<int:childcomment_id>/', views.CommentDelete.as_view()),
    path('comment/delete/<int:comment_id>/', views.CommentDelete.as_view()),
]