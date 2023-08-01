from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import LoginSerializer, SignupSerializer, RefreshTokenSerializer, ProfileSerializer

# Create your views here.

User = get_user_model()


@permission_classes([AllowAny])
class SingupView(APIView):

    throttle_scope = 'signup'

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response("회원가입에 성공했습니다.", status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class LoginView(APIView):

    throttle_scope = 'normal'

    # @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": {"id":user.pk, "nickname": user.nickname},
                    "message": "login success",
                    "access_token": access_token
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
        # try:
        # 요청 데이터에서 refresh 토큰을 가져옵니다.
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        else:
            return Response('Refresh 토큰이 제공되지 않았습니다.', status=status.HTTP_400_BAD_REQUEST)
        response = Response({'message': '로그아웃 성공'})
        response.set_cookie('refresh', '', httponly=True, samesite='None', secure=True)
        return response


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
                "user": {"id":user.pk, "nickname": user.nickname}
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
