from rest_framework import serializers
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
            username=username, password=password
        )
        if user is None:
            raise serializers.ValidationError('아이디나 비밀번호가 올바르지 않습니다.')
        
        if not user.is_active:
            raise serializers.ValidationError('휴먼유저입니다.')
        
        return { "username": username, "password": password, "user":user }