"""PartyJoinRequest model."""

# Django
from django.db import models

# Utils
from api.utils.models import BaseModel


class PartyJoinRequest(BaseModel):
    """PartyJoinRequest model.

    Not member users to a party can request to join 
    """

    class Meta:
        db_table = 'parties_join_requests'

    party = models.ForeignKey('parties.Party', on_delete=models.CASCADE)

    requested_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='User that is requesting to join',
        related_name='requested_by'
    )

    message = models.CharField(
        'Party join request message', max_length=255, blank=True
    )

    def __str__(self):
        return f"@{self.issued_by.username} request join #{self.party.slug_name}"
