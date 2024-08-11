"""Tournament Model."""

# Django
from django.db import models


class Tournament(models.Model):

    class Meta:
        db_table = 'tournaments'

    name = models.CharField(max_length=60)

    image = models.CharField(max_length=255)

    start_date = models.DateField(null=True, blank=True)

    is_finished = models.BooleanField(default=False)
