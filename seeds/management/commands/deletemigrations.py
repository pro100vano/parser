from django.core.management.base import BaseCommand

# python manage.py seed --mode=refresh


class Command(BaseCommand):
    help = "Delete all app_ tables, seeds and migrations"

    def handle(self, *args, **options):
        # self.stdout.write("[DONE]\n")
        pass
