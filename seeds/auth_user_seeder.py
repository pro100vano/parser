import os
import sys

from django.contrib.auth.models import User
from django.utils.timezone import now


class AuthUserSeeder:

    def create(self, refresh=False):
        if refresh is True:
            self.truncate_table()

        self.create_superuser()

    # TRUNCATE TABLE
    def truncate_table(self):
        User.objects.all().delete()
        sys.stdout.write("Truncate auth_user table ... [OK]\n")

    # CREATE SUPERUSER
    def create_superuser(self):
        if bool(User.objects.filter(username='admin').count()):
            sys.stdout.write('User admin already exists!\n')
            return False
        else:
            u = User(
                id=1,
                is_superuser=True,
                username='admin',
                first_name='firstName',
                last_name='lastName',
                email='superadmin@admin.com',
                is_staff=True,
                is_active=True,
                date_joined=now()
            )
            u.set_password(os.getenv('SUPERUSER_PASS', 'rootroot007'))
            u.save()

            sys.stdout.write("User admin created successfully! [OK]\n")
            return u.id
