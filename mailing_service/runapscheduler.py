import smtplib
from datetime import datetime, timedelta

import pytz as pytz
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore

from mailing_service.models import Newsletter, NewsletterTry

logger = logging.getLogger(__name__)


# Функция старта периодических задач
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()


# Главная функция по отправке рассылки
def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    newsletters = Newsletter.objects.all()

    for newsletter in newsletters:
        if newsletter.start_time < current_datetime < newsletter.end_time or newsletter.status == 'завершена':
            clients = newsletter.client.all()
            clients_emails = [clients.email for clients in clients]
            message_subject = newsletter.message.subject
            message_body = newsletter.message.body

            newsletter.status = 'запущена'
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

            if newsletter.frequency == 'раз в день':
                newsletter.start_time += timedelta(days=1, hours=0, minutes=0)
            elif newsletter.frequency == 'раз в неделю':
                newsletter.start_time += timedelta(days=7, hours=0, minutes=0)
            elif newsletter.frequency == 'раз в месяц':
                newsletter.start_time += timedelta(days=30, hours=0, minutes=0)

        elif current_datetime > newsletter.end_time or newsletter.start_time > newsletter.end_time:
            newsletter.status = 'завершена'

        elif current_datetime < newsletter.start_time:
            newsletter.status = 'создана'

        newsletter.save()


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_mailing(),
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="mailing",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'mailing'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
