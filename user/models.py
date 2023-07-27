from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.utils.deconstruct import deconstructible

import uuid


@deconstructible
class UploadToPath:
    def __call__(self, instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4().hex}.{extension}"
        return f"profile/{instance.pk}/{unique_filename}"


# class UserManager(BaseUserManager):

#     def _create_user(self, username, password, nickname, is_staff, is_superuser, **extra_fields):
#         if not username:
#             raise ValueError('User must have an username')
#         now = timezone.localtime()
#         user = self.model(
#             username = username,
#             nickname = nickname,
#             is_staff = is_staff,
#             is_active = True,
#             is_superuser = is_superuser,
#             last_login = now,
#             date_joined = now,
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)  
#         return user
    
#     def create_user(self, username, password, nickname, **extra_fields):
#         return self._create_user(username, password, nickname, False, False, **extra_fields)
    
#     def create_superuser(self, username, password, nickname, **extra_fields):
#         return self._create_user(username, password, nickname, True, True, **extra_fields)


class User(AbstractUser):
    nickname = models.CharField(max_length=15)
    image = models.ImageField(upload_to=UploadToPath(), default='/my_profile.png')
    first_name = None
    last_name = None

    REQUIRED_FIELDS = ['nickname']

    # objects = UserManager()

    def __str__(self):
        return self.nickname