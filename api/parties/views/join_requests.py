# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Serializers
from api.parties.serializers import JoinRequestModelSerializer, PartyAceeptJoinRequestSerializer

# Models
from api.parties.models import PartyJoinRequest

# Permissions
from api.parties.permissions import IsPartyAdmin


class JoinRequestViewSet(viewsets.GenericViewSet):
    lookup_field = 'id'
    serializer_class = JoinRequestModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['accept', 'reject']:
            permissions.append(IsPartyAdmin)
        return [permission() for permission in permissions]

    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        join_request = get_object_or_404(PartyJoinRequest, id=kwargs['id'])
        self.check_object_permissions(self.request, join_request.party)

        serializer = PartyAceeptJoinRequestSerializer(
            data={'join_request': join_request.id}
        )
        serializer.is_valid()
        serializer.save()

        return Response({'message': 'Join request has been aceepted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, *args, **kwargs):
        join_request = get_object_or_404(PartyJoinRequest, id=kwargs['id'])
        self.check_object_permissions(self.request, join_request.party)

        join_request.delete()

        return Response({'message': 'Join request has been rejected'}, status=status.HTTP_200_OK)
