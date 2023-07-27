import jwt
from decouple import config


def get_user_from_jwt(token):
    try:
        decoded_token = jwt.decode(token, config('SECRET_KEY'), algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        # 이제 user_id를 사용하여 유저 정보를 조회하거나 처리할 수 있습니다.
        # 예를 들어, User 모델에서 해당 user_id를 가진 유저를 가져올 수 있습니다.
        # user = User.objects.get(pk=user_id)
        return user_id
    except jwt.ExpiredSignatureError:
        # 토큰이 만료된 경우 처리
        return None
    except jwt.InvalidTokenError:
        # 토큰이 유효하지 않은 경우 처리
        return None