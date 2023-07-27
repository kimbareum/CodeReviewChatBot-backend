from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from decouple import config
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTFromCookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the access_token cookie
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return None

        # Call the JWTAuthentication's authenticate method
        try:
            decode = jwt.decode(access_token, config('SECRET_KEY'), algorithms=["HS256"])
            user = User.objects.get(pk=decode.get('user_id'))
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        return (user, None)