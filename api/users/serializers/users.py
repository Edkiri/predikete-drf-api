# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Serializers
from .profiles import ProfileModelSerializer

# Models
from api.users.models import User, Profile

# Utilities
import jwt
from datetime import timedelta
import logging

# Configura el logger
logger = logging.getLogger(__name__)


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'profile'
        )
        read_only_fields = ('email', 'profile', 'username', 'id',)


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError(
                'This account is not verified yet :(')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user_id': self.context['user'].id,
            'exp': int(exp_date.timestamp()),
            'type': 'access_token'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return self.context['user'], token


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data calidation and user/profile creation
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(
            **data, is_verified=False, is_client=True)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """Send account verification link to given user."""
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(
            user.username)
        from_email = 'eduardokiriakos@gmail.com'
        content = render_to_string(
            'account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(
            subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """Create JWT token that the user can use to verify its account."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""

        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verifies status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
