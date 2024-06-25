import smtplib
from datetime import datetime

import pytz
from django.core.mail import send_mail
from django.core.management import BaseCommand

from config import settings
from mailing_service.models import Newsletter, NewsletterTry


class Command(BaseCommand):

    def handle(self, *args, **options):
        """"""
        newsletters = Newsletter.objects.all()
        print('Доступны следующие рассылки: ')
        for newsletter in newsletters:
            print(newsletter)
        number = int(input('Введите номер рассылки для мгновенной отправки: '))
        if number in [nl.pk for nl in newsletters]:
            print('Отправка рассылки...')
            self.permanent_send(number)

        else:
            print('Убедитесь, что номер рассылки введён корректно')

    @staticmethod
    def permanent_send(pk):
        """Метод для отправки выбранной рассылки"""
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        newsletter = Newsletter.objects.get(pk=pk)
        clients = newsletter.client.all()
        clients_emails = [clients.email for clients in clients]
        message_subject = newsletter.message.subject
        message_body = newsletter.message.body
        try:
            send_mail(
                subject=message_subject,
                message=message_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=clients_emails,
                fail_silently=False
            )
            success = True
            response = 'Рассылка успешно отправлена'
        except smtplib.SMTPException as e:
            success = False
            response = f'Ошибка при отправке письма: {str(e)}'
        finally:
            new = NewsletterTry.objects.create(
                last_try_time=current_datetime,
                success=success,
                response=response,
                newsletter=newsletter,
            )
            new.client.add(*clients)
            new.save()
