from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name='email', unique=True)
    fullname = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.fullname} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Newsletter(models.Model):
    start_time = models.DateTimeField(verbose_name='время начала рассылки')
    end_time = models.DateTimeField(verbose_name='время окончания рассылки')

    daily = 'раз в день'
    weekly = 'раз в неделю'
    monthly = 'раз в месяц'
    mailing_frequencies = [(daily, 'раз в день'), (weekly, 'раз в неделю'), (monthly, 'раз в месяц')]
    frequency = models.CharField(max_length=50, verbose_name='частота рассылки', choices=mailing_frequencies)

    created = 'создана'
    started = 'запущена'
    completed = 'завершена'
    newsletter_status = [(created, 'создана'), (started, 'запущена'), (completed, 'завершена')]
    status = models.CharField(max_length=50, verbose_name='статус рассылки', choices=newsletter_status, default=created)

    client = models.ManyToManyField(Client, verbose_name='клиент', **NULLABLE)
