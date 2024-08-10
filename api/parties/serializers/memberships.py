
# Django REST Framework
from rest_framework import serializers

# Models
from api.parties.models import Party, PartyMembership
from api.users.models import User

# Serializers
from api.users.serializers import UserModelSerializer


class PartyMembershipModelSerializer(serializers.ModelSerializer):

    user = UserModelSerializer(read_only=True)

    class Meta:
        model = PartyMembership

        fields = ('user', 'is_admin',)
        read_only_fields = ('user',)


class PartyAddMemberSerializer(serializers.Serializer):

    party = serializers.PrimaryKeyRelatedField(
        queryset=Party.objects.all()
    )

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    def validate(self, data):
        if data['party'].members.filter(id=data['user'].id).exists():
            raise serializers.ValidationError(
                "User is already member of this group.")

        return data

    def save(self):
        PartyMembership.objects.create(
            user=self.validated_data['user'],
            party=self.validated_data['party']
        )
