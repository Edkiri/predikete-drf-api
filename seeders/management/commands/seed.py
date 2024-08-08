# Django
from django.core.management.base import BaseCommand

# Models
from api.users.models import User, Profile
from api.tournaments.models import Tournament

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        
        # Admin user
        # admin = User.objects.create(
        #     username='eduk',
        #     first_name="Eduardo",
        #     last_name='Kiriakos',
        #     email='eduardokiriakos@gmail.com',
        # )
        # admin.set_password('Admin123...')
        # admin.is_superuser = True
        # admin.is_verified = True
        # admin.is_staff = True
        # admin.save()

        # Profile.objects.create(
        #     user_id=admin.id
        # )

        self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Tournament
        # Tournament.objects.create(name='Mundial FIFA 2026')
        
        self.stdout.write(self.style.SUCCESS('Test tournamet created'))