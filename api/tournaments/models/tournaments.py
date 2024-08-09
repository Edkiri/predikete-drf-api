"""Tournament Model."""

# Django
from django.db import models

# Models
from api.utils.models import BaseModel


class Tournament(BaseModel):

    class Meta:
        db_table = 'tournaments'

    name = models.CharField(max_length=60)

    image = models.CharField(max_length=255)

    is_finished = models.BooleanField(default=False)
