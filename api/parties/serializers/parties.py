"""Parties serializers."""

# Django
from django.utils.text import slugify

# Django REST Framework
from rest_framework import serializers

# Model
from api.parties.models import Party
from api.tournaments.models import Tournament

# Serializers
from .memberships import PartyMembershipModelSerializer
from api.tournaments.serializers import TournamentModelSerializer


class PartyModelSerializer(serializers.ModelSerializer):
    """Parties model serializer."""

    tournament = TournamentModelSerializer(read_only=True)

    members = PartyMembershipModelSerializer(
        source="memberships",
        read_only=True,
        many=True
    )

    name = serializers.CharField(min_length=4, max_length=50)

    max_members = serializers.IntegerField(min_value=5, max_value=100)

    class Meta:
        """Meta class."""

        model = Party

        fields = (
            'name',
            'slug_name',
            'about',
            'picture',
            'is_public',
            'tournament',
            'max_members',
            'members'
        )
        read_only_fields = ('slug_name', 'members', 'slug_name', 'tournament',)

    def update(self, instance, validated_data):
        name = validated_data.get('name')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if name:
            instance.slug_name = slugify(name)

        instance.save()
        return instance


class PartyCreateSerializer(serializers.ModelSerializer):
    """Create Party serializer"""

    tournament = serializers.PrimaryKeyRelatedField(
        queryset=Tournament.objects.all()
    )

    name = serializers.CharField(min_length=4, max_length=50)

    max_members = serializers.IntegerField(min_value=5, max_value=100)

    class Meta:
        model = Party

        fields = (
            'name',
            'slug_name',
            'about',
            'picture',
            'is_public',
            'tournament',
            'max_members',
        )
        read_only_fields = ('slug_name',)

    def create(self, validated_data):
        name = validated_data.get('name')
        slug_name = slugify(name)
        validated_data['slug_name'] = slug_name
        return super().create(validated_data)
