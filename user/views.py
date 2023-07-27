from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import LoginSerializer

# Create your views here.

User = get_user_model()


@permission_classes([AllowAny])
class LoginView(APIView):

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

            response.set_cookie("refresh_token", refresh_token, httponly=True, samesite='None', secure=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        # try:
        # 요청 데이터에서 refresh 토큰을 가져옵니다.
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # RefreshToken 클래스를 사용하여 refresh 토큰 문자열을 파싱합니다.
            token = RefreshToken(refresh_token)
            token.blacklist()
        else:
            return Response({'error': 'Refresh 토큰이 제공되지 않았습니다.'}, status=400)
        response = Response({'message': '로그아웃 성공'}, status=200)
        response.set_cookie('refresh_token', '', httponly=True, samesite='None', secure=True)
        return response


@permission_classes([AllowAny])
class RefreshTokenView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"error": "Refresh Token이 없습니다."}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            user = User.objects.get(pk=access_token.get('user_id'))
            response = Response({
                "access_token": str(access_token),
                "user": {"id":user.pk, "nickname": user.nickname}
                })
            return response
        except Exception as e:
            return Response("유효하지 않은 Refresh Token입니다.", status=400)