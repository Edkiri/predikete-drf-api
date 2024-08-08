"""User models."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utils
from api.utils.models import BaseModel


class User(BaseModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    class Meta:
        db_table = 'users'

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client',
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries. '
            'clients are the main type of user.'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email address.'
    )

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Set to False when the user delete his account'
    )

    def __str__(self):
        """Return username."""
        return self.username
