"""Party model."""

# Django
from django.db import models


class Party(models.Model):
    """Party model.

    A party is a private group where members can make predictions
    related to a tournament. To join a party, a user must receive a unique
    invitation code from an existing party member or make a request to join.
    """

    class Meta:
        db_table = 'parties'

    name = models.CharField('party name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    tournament = models.ForeignKey(
        'tournaments.Tournament',
        on_delete=models.CASCADE
    )

    about = models.CharField('party description', max_length=255)
    picture = models.CharField('party image', max_length=255)

    max_members = models.IntegerField('party max members', default=50)

    members = models.ManyToManyField(
        'users.User',
        through='parties.PartyMembership',
        through_fields=('party', 'user')
    )

    is_public = models.BooleanField(
        default=True,
        help_text='Public parties are listed in the main page so everyone know about their existence.'
    )

    def __str__(self):
        """Return circle name."""
        return self.name
