# Django
from django.db import transaction

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Model
from api.parties.models import PartyJoinInvitation, PartyMembership

# Serializers
from api.parties.serializers import InvitationModelSerializer

# Permissions
from api.parties.permissions import IsInvitationOwner


class InvitationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    lookup_field = 'id'
    serializer_class = InvitationModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['accept', 'reject']:
            permissions.append(IsInvitationOwner)
        return [permission() for permission in permissions]

    def get_queryset(self):
        """get user invitations."""
        return PartyJoinInvitation.objects.filter(issued_to=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                invitation = get_object_or_404(
                    PartyJoinInvitation, id=kwargs['id'])
                PartyMembership.objects.create(
                    party=invitation.party,
                    user=invitation.issued_to,
                )
                invitation.delete()
                return Response(
                    {'message': 'You have successfully joined the party'},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {'error': 'An error occurred while accepting the invitation. Please try again.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def reject(self, request, *args, **kwargs):
        invitation = get_object_or_404(PartyJoinInvitation, id=kwargs['id'])
        invitation.delete()
        return Response(
            {'message': 'You have successfully rejected the invitation party'},
            status=status.HTTP_200_OK
        )
