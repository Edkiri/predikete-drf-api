# Django REST Framework
from rest_framework import serializers

# Model
from api.tournaments.models import Tournament


class TournamentModelSerializer(serializers.ModelSerializer):
    """Tournament model serializer."""

    class Meta:
        model = Tournament

        fields = ('id', 'name', 'image', 'is_finished')
        read_only_fields = ('id', 'is_finished')
