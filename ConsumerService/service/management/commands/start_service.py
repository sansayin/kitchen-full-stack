from django.core.management.base import BaseCommand
from service.threading_service import UserCreatedServant


class Command(BaseCommand):
    help = "Launches Listener for user_created message : Kafka"

    def handle(self, *args, **options):
        td = UserCreatedServant()
        td.start()
        self.stdout.write("Started Consumer Thread")
