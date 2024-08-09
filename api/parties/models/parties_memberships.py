"""Membership model."""

# Django
from django.db import models


class PartyMembership(models.Model):
    """Membership model.

    A membership is the table that holds the relationship between
    a user and a party.
    """

    class Meta:
        db_table = 'parties_memberships'

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    party = models.ForeignKey(
        'parties.Party',
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    is_admin = models.BooleanField(
        'party admin',
        default=False,
        help_text="Party admins can update the party's data and manage its members."
    )

    def __str__(self):
        """Return username and party."""
        return '@{} at #{}'.format(
            self.user.username,
            self.party.slug_name
        )
