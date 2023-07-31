from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta(object):
        model = User
        fields = ['username', 'password', 'password2', 'nickname']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "비밀번호가 서로 다릅니다."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            nickname=validated_data.get('nickname'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'username': {'validators': []}, 
        }

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username:
            raise serializers.ValidationError('아이디는 필수 입력값입니다.')
        
        if not password:
            raise serializers.ValidationError('패스워드는 필수 입력값입니다.')

        user = authenticate(
            username=username, password=password
        )
        if user is None:
            raise serializers.ValidationError('아이디나 비밀번호가 올바르지 않습니다.')
        
        if not user.is_active:
            raise serializers.ValidationError('휴먼유저입니다.')
        
        return { "username": username, "password": password, "user":user }


class RefreshTokenSerializer(serializers.Serializer):

    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        
        try:
            refresh = self.token_class(attrs["refresh"])
        except:
            raise serializers.ValidationError('유효하지 않거나 만료된 토큰입니다.')
        access = refresh.access_token
        data = {"access": str(refresh.access_token)}

        try:
            user = User.objects.get(pk=access.get('user_id'), is_active=True)
        except:
            raise serializers.ValidationError("유저가 존재하지 않습니다.")
        data['user'] = user

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)
            
        return data


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['nickname', 'image']