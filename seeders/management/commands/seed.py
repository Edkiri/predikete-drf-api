# Django
from django.core.management.base import BaseCommand

# Models
from api.users.models import User, Profile
from api.tournaments.models import Tournament
from api.parties.models import Party, PartyMembership

# Utils
from decouple import config


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):

        # Admin user
        edu = User.objects.create(
            username='eduk',
            first_name="Eduardo",
            last_name='Kiriakos',
            email=config('ADMIN_EMAIL'),
        )
        edu.set_password(config('ADMIN_PASSWORD'))
        edu.is_superuser = True
        edu.is_verified = True
        edu.is_staff = True
        edu.save()
        Profile.objects.create(
            user_id=edu.id
        )
        ori = User.objects.create(
            username='orik',
            first_name="Oriana",
            last_name='Kiriakos',
            email='ori@mail.com',
        )
        ori.set_password('Admin123...')
        ori.is_superuser = False
        ori.is_staff = False
        ori.is_verified = True
        ori.save()
        Profile.objects.create(
            user_id=ori.id
        )
        self.stdout.write(self.style.SUCCESS('users created'))

        # Tournament
        tournament = Tournament.objects.create(name='Mundial FIFA 2026')
        self.stdout.write(self.style.SUCCESS('tournament created'))

        # Parties
        edu_party = Party.objects.create(
            name='La Familia',
            slug_name='la-familia',
            picture='familia.png',
            tournament=tournament
        )
        PartyMembership.objects.create(
            user=edu,
            party=edu_party,
            is_admin=True,
        )
        ori_party = Party.objects.create(
            name='La Familia de Ori',
            slug_name='la-familia-de-ori',
            picture='familia-de-ori.png',
            tournament=tournament
        )
        PartyMembership.objects.create(
            user=ori,
            party=ori_party,
            is_admin=True,
        )
        self.stdout.write(self.style.SUCCESS('parties created'))
