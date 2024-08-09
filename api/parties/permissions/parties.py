"""Parties permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from api.parties.models import PartyMembership, PartyJoinInvitation

class IsPartyMember(BasePermission):
    """Allow access only to party members.

    Expect that the views implementing this permission
    have a 'party' attribute assigned.
    """

    def has_object_permission(self, request, view, obj):
        """Verify user is an active member of the party."""
        try:
            PartyMembership.objects.get(
                user=request.user,
                party=obj
            )
        except PartyMembership.DoesNotExist:
            return False
        return True


class IsPartyAdmin(BasePermission):
    """Allow access only to party admins.

    Expect that the views implementing this permission
    have a 'party' attribute assigned.
    """

    def has_object_permission(self, request, view, obj):
        """Verify user is an admin member of the party."""
        try:
            membership = PartyMembership.objects.get(
                user=request.user,
                party=obj
            )
            if membership.is_admin == True:
                return True
            return False
        except PartyMembership.DoesNotExist:
            return False


class IsInvitationOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            PartyJoinInvitation.objects.get(
                user=request.user,
                party=obj
            )
        except PartyMembership.DoesNotExist:
            return False
        return True
