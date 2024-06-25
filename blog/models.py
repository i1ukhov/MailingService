from django.db import models

NULLABLE = {"blank": True, "null": True}


class Article(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Добавьте содержимое",
    )
    preview = models.ImageField(
        upload_to="blog/images",
        verbose_name="Превью",
        help_text="Загрузите изображение",
        **NULLABLE,
    )
    views_count = models.IntegerField(
        verbose_name="Количество просмотров",
        help_text="Добавьте количество просмотров",
        default=0,
        **NULLABLE,
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Добавьте дату создания",
    )
