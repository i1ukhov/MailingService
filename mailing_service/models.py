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


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='тема сообщения')
    body = models.TextField(verbose_name='текст сообщения')

    def __str__(self):
        return f'Сообщение №{self.pk}. Тема: {self.subject}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Newsletter(models.Model):
    start_time = models.DateTimeField(verbose_name='время начала рассылки')
    end_time = models.DateTimeField(verbose_name='время окончания рассылки', **NULLABLE)

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

    client = models.ManyToManyField(Client, verbose_name='клиент', blank=True)
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING, verbose_name='сообщение', **NULLABLE)

    def __str__(self):
        return f'Рассылка №{self.pk}. Время: {self.start_time} - {self.end_time}. Статус: {self.status}. Частота: {self.frequency}.'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class NewsletterTry(models.Model):
    last_try_time = models.DateTimeField(verbose_name='дата и время последней попытки рассылки')
    success = models.BooleanField(verbose_name='результат рассылки')
    response = models.TextField(verbose_name='ответ сервера', **NULLABLE)

    newsletter = models.ForeignKey(Newsletter, on_delete=models.DO_NOTHING, verbose_name='рассылка')
    client = models.ManyToManyField(Client, verbose_name='клиенты', blank=True)

    def __str__(self):
        return f'Попытка рассылки №{self.pk}. Дата и время: {self.last_try_time}. Результат: {self.success}.'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
