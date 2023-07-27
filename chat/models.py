from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Chat(models.Model):
    title = models.CharField(max_length=30)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'
    

# class ChatList(models.Model):
#     ROLE_CHOICES = [
#         ('user', 'user'),
#         ('assistant', 'assistant')
#     ]

#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     ROLE = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     prompt = models.TextField()