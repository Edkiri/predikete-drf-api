"""PartyJoinInvitation model."""

# Django
from django.db import models

# Utils
from api.utils.models import BaseModel


class PartyJoinInvitation(BaseModel):
    """PartyJoinInvitation model.

    A party invitation can be sent by admin members of a party
    """

    class Meta:
        db_table = 'parties_join_invitations'

    party = models.ForeignKey('parties.Party', on_delete=models.CASCADE)

    issued_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='Party member that is providing the invitation',
        related_name='issued_by'
    )

    issued_to = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='User that has been invited to the party',
        related_name='issued_to'
    )

    message = models.CharField(
        'invitation message', max_length=255, blank=True
    )

    def __str__(self):
        return f"#{self.party.slug_name} invitation from @{self.issued_by.username} to @{self.issued_to.username}"
