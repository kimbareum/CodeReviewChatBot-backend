from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from django.contrib.auth import get_user_model
from .serializers import LoginSerializer, SignupSerializer, RefreshTokenSerializer

# Create your views here.

User = get_user_model()


@permission_classes([AllowAny])
class SingupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response("회원가입에 성공했습니다.", status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class LoginView(APIView):

    @method_decorator(ensure_csrf_cookie)
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

            print(response.cookies)
            response.set_cookie("refresh", refresh_token, httponly=True, samesite='None', secure=True)
            return response
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class LogoutView(APIView):

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


# @permission_classes([AllowAny])
# class RefreshTokenView(APIView):

#     def post(self, request):
#         refresh_token = request.COOKIES.get('refresh')

#         if not refresh_token:
#             return Response("Refresh Token이 없습니다.", status=status.HTTP_400_BAD_REQUEST)
        
#         # tokenSerializer = RefreshTokenSerializer(data=request.COOKIES)

#         # # if tokenSerializer.is_valid(raise_exception=True):
#         # #     print(tokenSerializer.data)

#         try:
#             refresh = RefreshToken(refresh_token)
#             access_token = refresh.access_token
#             user = User.objects.get(pk=access_token.get('user_id'))
#             response = Response({
#                 "access_token": str(access_token),
#                 "user": {"id":user.pk, "nickname": user.nickname}
#                 })
#             return response
#         except Exception as e:
#             return Response("유효하지 않은 Refresh Token입니다.", status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])
class RefreshTokenView(APIView):

    @method_decorator(ensure_csrf_cookie)
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