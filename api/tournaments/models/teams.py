from django.db import models


class Team(models.Model):

    class Meta:
        db_table = 'teams'

    name = models.CharField(max_length=100)

    image = models.CharField(max_length=100)

    def __str__(self):
        return self.name
