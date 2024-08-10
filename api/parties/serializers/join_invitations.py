# Django
from django.db import transaction

# Django REST Framework
from rest_framework import serializers

# Models
from api.parties.models import PartyJoinInvitation, PartyMembership, PartyJoinInvitation
from api.users.models import User

# Serializers
from api.users.serializers import UserModelSerializer
from api.parties.serializers import PartyModelSerializer


class InvitationModelSerializer(serializers.ModelSerializer):

    issued_by = UserModelSerializer(read_only=True)
    issued_to = UserModelSerializer(read_only=True)
    party = PartyModelSerializer(read_only=True)

    class Meta:
        model = PartyJoinInvitation

        fields = (
            'id',
            'party',
            'issued_by',
            'message',
            'issued_to',
            'created',
        )


class PartyInviteUserSerializer(serializers.Serializer):

    issued_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    message = serializers.CharField(
        max_length=100, required=False, allow_blank=True)

    def validate_issued_to(self, data):
        """Verify user isn't already a member."""
        user = data
        party = self.context['party']

        if user.id == self.context['request'].user.id:
            raise serializers.ValidationError(
                "User can not invite himself to a party"
            )

        membership = PartyMembership.objects.filter(party=party, user=user)
        if membership.exists():
            raise serializers.ValidationError(
                "User is already member of this party"
            )

        join_invitation = PartyJoinInvitation.objects.filter(
            party=party, issued_to=user)
        if join_invitation.exists():
            raise serializers.ValidationError(
                "User already has been invited"
            )

        return data

    def save(self):
        message = self.validated_data.get('message', '')

        return PartyJoinInvitation.objects.create(
            party=self.context['party'],
            issued_by=self.context['request'].user,
            issued_to=self.validated_data['issued_to'],
            message=message,
        )
