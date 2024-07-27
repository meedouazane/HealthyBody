from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
import uuid
from django.conf import settings


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sex = models.CharField(null=True, max_length=100)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        """ return string object"""
        return self.email


class Records(models.Model):
    """ User table """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    data = models.DateField(default=timezone.now)
    bmi = models.FloatField()

    def __str__(self):
        """ return string object"""
        return self.user_id