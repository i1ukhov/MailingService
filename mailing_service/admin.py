from django.contrib import admin
from mailing_service.models import Client, Message, Newsletter, NewsletterTry


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'comment')
    search_fields = ('email', 'fullname')
    list_filter = ('email', 'fullname')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    search_fields = ('subject', 'body')
    list_filter = ('subject', 'body')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'frequency', 'status')
    search_fields = ('start_time', 'end_time', 'frequency', 'status', 'client', 'message')
    list_filter = ('start_time', 'end_time', 'status', 'client')


@admin.register(NewsletterTry)
class NewsletterTryAdmin(admin.ModelAdmin):
    list_display = ('success', 'response', 'newsletter', 'client')
    search_fields = ('last_time_try', 'success', 'response', 'newsletter', 'client')
    list_filter = ('success', 'response', 'newsletter', 'client')
