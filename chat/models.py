from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.db.models import Q

from django.utils import timezone
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
    
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created_at = timezone.now()
    #     self.updated_at = timezone.now()
    #     super(Chat, self).save(*args, **kwargs)


class ActiveCommentManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(Q(is_deleted=False) | (Q(is_deleted=True) & Q(child_count__gte=1)))


class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    child_count = models.IntegerField(default=0)

    all_objects = models.Manager()
    objects = ActiveCommentManager()
    

    def __str__(self):
        return f'{self.chat.title}/{self.content}'


class ActiveChildCommentManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)


class ChildComment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='child_comments')

    all_objects = models.Manager()
    objects = ActiveChildCommentManager()

    def __str__(self):
        return f'{self.parent_comment.content}/{self.content}'
