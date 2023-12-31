from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import LoginSerializer, SignupSerializer, RefreshTokenSerializer, ProfileSerializer, UserDeleteSerializer, PasswordChangeSerializer

# Create your views here.

User = get_user_model()


### 유저 인증
@permission_classes([AllowAny])
class SingupView(APIView):

    throttle_scope = 'signup'

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response("회원가입에 성공했습니다.", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class LoginView(APIView):

    throttle_scope = 'normal'

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": {"id":user.pk, "nickname": user.nickname, "image": user.image.url},
                    "message": "login success",
                    "access_token": access_token,
                },
                status=status.HTTP_200_OK
            )
            
            response.set_cookie("refresh", refresh_token, httponly=True, samesite='None', secure=True)
            return response
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class LogoutView(APIView):

    throttle_scope = 'normal'

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        else:
            return Response('Refresh 토큰이 제공되지 않았습니다.', status=status.HTTP_400_BAD_REQUEST)
        response = Response('로그아웃 성공')
        response.set_cookie('refresh', '', httponly=True, samesite='None', secure=True)
        return response


class UserDeleteView(APIView):

    throttle_scope = 'normal'

    def post(self, request):
        user = request.user

        serializer = UserDeleteSerializer(data=request.data, context={"user":user})
        if serializer.is_valid():
            user.is_active = False
            user.save()
            return Response("회원 비활성화에 성공했습니다.")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):

    throttle_scope = 'normal'

    def post(self, request):
        user = request.user

        serializer = PasswordChangeSerializer(data=request.data, context={"user":user})
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            user.set_password(password)
            user.save()
            response = Response("비밀번호 변경에 성공했습니다.")
            response.set_cookie("refresh", '', httponly=True, samesite='None', secure=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### 토큰
@permission_classes([AllowAny])
class RefreshTokenView(APIView):

    throttle_scope = 'normal'

    # @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        
        tokenSerializer = RefreshTokenSerializer(data=request.COOKIES)
        
        if tokenSerializer.is_valid():
            access_token = tokenSerializer.validated_data.get('access')
            refresh_token = str(tokenSerializer.validated_data.get('refresh'))
            user = tokenSerializer.validated_data.get('user')

            response = Response({
                "access_token": str(access_token),
                "user": {"id":user.pk, "nickname": user.nickname, "image": user.image.url}
                })
            response.set_cookie("refresh", refresh_token, httponly=True, samesite='None', secure=True)
            return response
        
        return Response("유효하지 않은 Refresh Token입니다.", status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):

    throttle_scope = 'normal'

    def get(self, request):
        user = request.user
        serialized_profile = ProfileSerializer(user)
        return Response(serialized_profile.data)
    
    def post(self, request):
        user = request.user
        serialized_profile = ProfileSerializer(user, data=request.data)
        if serialized_profile.is_valid():
            serialized_profile.save()
            return Response(serialized_profile.data)
        
        return Response(serialized_profile.errors, status=status.HTTP_400_BAD_REQUEST)
