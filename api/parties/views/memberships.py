# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Permissions
from api.parties.permissions import IsPartyAdmin

# Serializers
from api.users.serializers import UserModelSerializer
from api.parties.serializers import PartyInviteUserSerializer, JoinRequestModelSerializer, PartyCreateJoinRequestSerializer

# Models
from api.parties.models import Party, PartyJoinRequest

import logging
logger = logging.getLogger(__name__)

class MembershipViewSet(viewsets.GenericViewSet):
    lookup_field = 'slug_name'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the party exists."""
        slug_name = kwargs['slug_name']
        self.party = get_object_or_404(Party, slug_name=slug_name)
        self.user = request.user
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action in ['invite', 'list_join_request']:
            permissions.append(IsPartyAdmin)
        return [permission() for permission in permissions]

    @action(detail=True, methods=['post'])
    def invite(self, request, *args, **kwargs):
        """Invite a user to a party"""
        serializer = PartyInviteUserSerializer(
            data=request.data,
            context={'party': self.party, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserModelSerializer(request.user).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def list_join_request(self, request, *args, **kwargs):
        party_join_requests = PartyJoinRequest.objects.filter(party=self.party)
        serializer = JoinRequestModelSerializer(
            data=party_join_requests, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def create_join_request(self, request, *args, **kwargs):
        """User request join to party"""
        serializer = PartyCreateJoinRequestSerializer(
            data=request.data,
            context={'party': self.party, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'You have successfully request to join this party'}, status=status.HTTP_200_OK)
