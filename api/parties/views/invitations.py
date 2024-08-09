# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

# Model
from api.parties.models import PartyJoinInvitation

# Serializers
from api.parties.serializers import InvitationModelSerializer


class InvitationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = InvitationModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_queryset(self):
        """get user invitations."""
        return PartyJoinInvitation.objects.filter(issued_to=self.request.user)
