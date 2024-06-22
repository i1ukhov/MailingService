from time import sleep

from django.apps import AppConfig


class MailingServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing_service'
    verbose_name = 'Управление рассылками'

    def ready(self):
        from mailing_service.runapscheduler import start
        sleep(2)
        start()
