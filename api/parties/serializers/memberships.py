
# Django REST Framework
from rest_framework import serializers

# Models
from api.parties.models import PartyMembership, PartyJoinInvitation
from api.users.models import User

# Serializers
from api.users.serializers import UserModelSerializer


class PartyMembershipModelSerializer(serializers.ModelSerializer):

    user = UserModelSerializer(read_only=True)

    class Meta:
        model = PartyMembership

        fields = ('user', 'is_admin',)
        read_only_fields = ('user',)


class PartyInviteUserSerializer(serializers.Serializer):

    issued_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

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
        return PartyJoinInvitation.objects.create(
            party=self.context['party'],
            issued_by=self.context['request'].user,
            issued_to=self.validated_data['issued_to']
        )
