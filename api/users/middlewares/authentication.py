import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return None

        try:
            prefix, token = auth.split(' ')
            if prefix.lower() != 'bearer':
                raise exceptions.AuthenticationFailed(
                    'Authorization header must start with Bearer')
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
        except (ValueError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')

        # Retrieve the user from the payload
        user_id = payload.get('user_id')
        if user_id is None:
            raise exceptions.AuthenticationFailed(
                'Token does not contain user_id')

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer'
