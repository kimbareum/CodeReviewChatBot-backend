from django.contrib import admin
from .models import Chat, Comment, ChildComment

# Register your models here.

admin.site.register(Chat)
admin.site.register(Comment)
admin.site.register(ChildComment)
