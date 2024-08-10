# Django
from django.db import transaction

# Django REST Framework
from rest_framework import serializers

# Models
from api.parties.models import PartyMembership, PartyJoinRequest

# Serializers
from api.users.serializers import UserModelSerializer
from api.parties.serializers import PartyModelSerializer, PartyAddMemberSerializer


class JoinRequestModelSerializer(serializers.ModelSerializer):

    party = PartyModelSerializer(read_only=True)
    requested_by = UserModelSerializer(read_only=True)

    class Meta:
        model = PartyJoinRequest

        fields = ('id', 'party', 'requested_by', 'message', 'created',)


class PartyCreateJoinRequestSerializer(serializers.Serializer):

    message = serializers.CharField(
        max_length=100, required=False, allow_blank=True)

    def validate(self, data):
        user = self.context['request'].user
        party = self.context['party']

        membership = PartyMembership.objects.filter(party=party, user=user)
        if membership.exists():
            raise serializers.ValidationError(
                "User is already member of this party"
            )

        join_request = PartyJoinRequest.objects.filter(
            party=party, requested_by=user)
        if join_request.exists():
            raise serializers.ValidationError(
                "User already has requested to join this party"
            )

        return data

    def save(self):
        message = self.validated_data.get('message', '')

        PartyJoinRequest.objects.create(
            party=self.context['party'],
            requested_by=self.context['request'].user,
            message=message,
        )


class PartyAceeptJoinRequestSerializer(serializers.Serializer):

    join_request = serializers.PrimaryKeyRelatedField(
        queryset=PartyJoinRequest.objects.all()
    )

    def save(self):
        join_request = self.validated_data['join_request']
        with transaction.atomic():
            add_member_serializer = PartyAddMemberSerializer(
                data={
                    'party': join_request.party.id,
                    'user': join_request.requested_by.id
                }
            )
            add_member_serializer.is_valid(raise_exception=True)
            add_member_serializer.save()
            join_request.delete()
