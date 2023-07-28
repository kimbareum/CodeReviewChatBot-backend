from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

# Create your models here.

User = get_user_model()


class ActiveManager(models.Manager):
    
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)


class Chat(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    all_objects = models.Manager()
    objects = ActiveManager()

    def __str__(self):
        return f'{self.title}'
