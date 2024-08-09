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
from api.parties.serializers import PartyInviteUserSerializer

# Models
from api.parties.models import Party

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
        """Assign permissions based on action."""
        permissions = [IsAuthenticated, IsPartyAdmin]
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
