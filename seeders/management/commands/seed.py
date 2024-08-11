# Django
from django.core.management.base import BaseCommand

# Models
from api.users.models import User, Profile
from api.tournaments.models import Tournament, Team, GroupStage, GroupStageDetails, Match
from api.parties.models import Party, PartyMembership

# Utils
from decouple import config

# Data
from .data import QatarTeams, GROUP_STAGES, MATCHES


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

        for team in QatarTeams:
            Team.objects.create(
                name=team.value,
                image=f"{team.value.lower()}.png"
            )
        self.stdout.write(self.style.SUCCESS('teams created'))

        for data in GROUP_STAGES:
            name = data.get('name')
            for team in data.get('teams'):
                group_stage = GroupStage.objects.create(
                    name=name,
                    tournament=tournament,
                    team=Team.objects.get(name=team)
                )
                GroupStageDetails.objects.create(group_stage=group_stage)

        self.stdout.write(self.style.SUCCESS('group stages created'))

        for match in MATCHES:
            Match.objects.create(
                tournament=tournament,
                home_team=Team.objects.get(name=match.get('home_team')),
                away_team=Team.objects.get(name=match.get('away_team')),
                date=match.get('date'),
                phase='Group Stage'
            )

        self.stdout.write(self.style.SUCCESS('group stages matches created'))
