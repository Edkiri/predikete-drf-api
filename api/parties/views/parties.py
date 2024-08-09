"""Parties views."""

# Django
from django.db import transaction

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from api.parties.permissions import IsPartyMember, IsPartyAdmin

# Serializers
from api.parties.serializers import PartyModelSerializer, PartyCreateSerializer

# Models
from api.parties.models import Party, PartyMembership

# Utils
import logging
logger = logging.getLogger(__name__)


class PartiesViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Party.objects.all()
    lookup_field = 'slug_name'

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', 'retrieve']:
            return PartyModelSerializer
        return PartyCreateSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action == 'retrieve':
            permissions.append(IsPartyMember)
        if self.action in ['update', 'partial_update', 'delete']:
            permissions.append(IsPartyAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        with transaction.atomic():
            party = serializer.save()
            user = self.request.user
            PartyMembership.objects.create(
                user=user,
                party=party,
                is_admin=True,
            )
