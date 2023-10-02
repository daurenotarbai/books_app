import re
from django.contrib.auth.models import update_last_login
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from auth.models import VerificationCode
from core.exceptions import EasyPassword, InvalidEmail, EmailAlreadyExist
from users.models import User


class UserSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=40)
    email = serializers.EmailField(max_length=40)

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if not data['email'] or "@" not in data['email']:
            raise InvalidEmail
        if len(data['password']) < 8:
            raise EasyPassword
        if not bool(re.match('^[a-zA-Z0-9-._]+@[a-zA-Z0-9]+\.[a-z]{1,3}$', data['email'])):
            raise InvalidEmail

        return data

    def create(self, validated_data):
        try:
            user = User(
                email=validated_data['email'],
                is_active=True
            )
            user.set_password(validated_data['password'])
            user.save()
        except IntegrityError as e:
            print(e)
            raise EmailAlreadyExist
        return user


class VerificationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerificationCode
        fields = ('email', 'code')


class TokenObtainPairsSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
