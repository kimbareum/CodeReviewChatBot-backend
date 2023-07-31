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


class User(AbstractUser):
    nickname = models.CharField(max_length=15)
    image = models.ImageField(upload_to=UploadToPath(), default='/default-user.png')
    first_name = None
    last_name = None

    REQUIRED_FIELDS = ['nickname']

    # objects = UserManager()

    def __str__(self):
        return self.nickname