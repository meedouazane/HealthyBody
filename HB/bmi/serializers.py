from rest_framework import serializers
from .models import CustomUser, Records
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ Serialize for User for authentication"""
    class Meta(object):
        model = User
        fields = ['id', 'username', 'email', 'password', 'sex', 'date_of_birth']


class BmiSerializer(serializers.ModelSerializer):
    """ Serialize for bmi model """
    class Meta:
        model = Records
        fields = ['id', 'bmi', 'height', 'weight', 'Classification']