
# Django REST Framework
from rest_framework.serializers import ModelSerializer

# Serializers
from api.users.serializers import UserModelSerializer

# Models
from api.parties.models import PartyMembership


class PartyMembershipModelSerializer(ModelSerializer):

    user = UserModelSerializer(read_only=True)

    class Meta:
        model = PartyMembership

        fields = ('user', 'is_admin',)
        read_only_fields = ('user',)
