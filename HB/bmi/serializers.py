from rest_framework import serializers
from .models import CustomUser, Records
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthSerializer(serializers.ModelSerializer):
    """ Serialize """
    class Meta(object):
        model = User
        fields = ['id', 'username', 'email', 'password', 'sex', 'date_of_birth']


class UserSerializer(serializers.ModelSerializer):
    """ Serialize """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'sex', 'date_of_birth']


class BmiSerializer(serializers.ModelSerializer):
    """ Serialize """
    class Meta:
        model = Records
        fields = ['id', 'bmi', 'height', 'weight']