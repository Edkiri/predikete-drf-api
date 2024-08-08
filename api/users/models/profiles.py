
"""Profile model."""
from django.db import models
from api.utils.models import BaseModel


class Profile(BaseModel):
    """Profile model.

    A profile holds a user's public data like biography,
    picture, and statistics.
    """

    class Meta:
        db_table = 'users_profiles'

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
