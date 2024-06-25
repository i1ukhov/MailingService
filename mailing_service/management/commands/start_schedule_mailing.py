from django.core.management import BaseCommand
from mailing_service.runapscheduler import send_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Запуск сервиса рассылок"""
        send_mailing()
