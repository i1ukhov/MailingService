from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name='email', unique=True)
    fullname = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    owner = models.ForeignKey(User, verbose_name="Кем создан",
                              help_text="Укажите кем создан клиент",
                              **NULLABLE,
                              on_delete=models.SET_NULL, )

    def __str__(self):
        return f'{self.fullname} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='тема сообщения')
    body = models.TextField(verbose_name='текст сообщения')

    owner = models.ForeignKey(User, verbose_name="Кем создано",
                              help_text="Укажите кем создано сообщение",
                              **NULLABLE,
                              on_delete=models.SET_NULL, )

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
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING, verbose_name='сообщение', blank=True)

    is_active = models.BooleanField(default=True, verbose_name='активность')

    owner = models.ForeignKey(User, verbose_name="Кем создана",
                              help_text="Укажите кем создана рассылка",
                              **NULLABLE,
                              on_delete=models.SET_NULL, )

    def __str__(self):
        return f'Рассылка №{self.pk}. Время: {self.start_time} - {self.end_time}. Статус: {self.status}. Частота: {self.frequency}.'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('can_view_newsletters', 'Can view newsletters'),
            ('can_view_clients', 'Can view clients'),
            ('can_block_newsletters', 'Can block newsletters'),
        ]


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
