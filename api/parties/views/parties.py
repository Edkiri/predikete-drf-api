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


class PartiesViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug_name'

    def get_queryset(self):
        """Restrict list to parties of the requesting user."""
        queryset = Party.objects.all()

        if self.action == 'list':
            queryset = queryset.filter(members=self.request.user).distinct()

        return queryset

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
