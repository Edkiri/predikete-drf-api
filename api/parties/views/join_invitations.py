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
from api.parties.serializers import InvitationModelSerializer, PartyAddMemberSerializer

# Permissions
from api.parties.permissions import IsInvitationOwner


class JoinInvitationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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
        invitation = get_object_or_404(PartyJoinInvitation, id=kwargs['id'])
        self.check_object_permissions(self.request, invitation)
        try:
            with transaction.atomic():
                add_member_serializer = PartyAddMemberSerializer(
                    data = {
                        'user': invitation.issued_to.id,
                        'party': invitation.party.id
                    }
                )
                add_member_serializer.is_valid(raise_exception=True)
                add_member_serializer.save()
                invitation.delete()
                return Response(
                    {'message': 'You have successfully joined the party'},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {'error': 'An error occurs'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def reject(self, request, *args, **kwargs):
        invitation = get_object_or_404(PartyJoinInvitation, id=kwargs['id'])
        self.check_object_permissions(self.request, invitation)
        invitation.delete()
        return Response(
            {'message': 'You have successfully rejected the invitation party'},
            status=status.HTTP_200_OK
        )
