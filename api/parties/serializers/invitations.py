# Django REST Framework
from rest_framework import serializers

# Model
from api.parties.models import PartyJoinInvitation

# Serializers
from api.users.serializers import UserModelSerializer
from api.parties.serializers import PartyModelSerializer


class InvitationModelSerializer(serializers.ModelSerializer):

    issued_by = UserModelSerializer(read_only=True)
    issued_to = UserModelSerializer(read_only=True)
    party = PartyModelSerializer(read_only=True)

    class Meta:
        model = PartyJoinInvitation
        
        fields = ('id', 'party', 'issued_by', 'message', 'issued_to', 'created',)
