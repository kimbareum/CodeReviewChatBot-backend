from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'username': {'validators': []},  # Disable uniqueness validation
        }

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username:
            raise serializers.ValidationError('아이디는 필수 입력값입니다.')
        
        if not password:
            raise serializers.ValidationError('패스워드는 필수 입력값입니다.')

        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )
        if user is None:
            raise serializers.ValidationError('아이디나 비밀번호가 올바르지 않습니다.')
        
        if not user.is_active:
            raise serializers.ValidationError('휴먼유저입니다.')
        
        return { "username": username, "password": password, "user":user }