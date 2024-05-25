from django.urls import path

from mailing_service.apps import MailingServiceConfig

from mailing_service.views import NewsletterListView, NewsletterUpdateView, NewsletterDeleteView, NewsletterCreateView, \
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, Homepage, MessageListView, MessageCreateView, \
    MessageUpdateView, MessageDeleteView, NewsletterTryListView

app_name = MailingServiceConfig.name

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    path('newsletters/', NewsletterListView.as_view(), name='newsletters_list'),
    path('newsletters/create', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletters/<int:pk>/update', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter/<int:pk>/delete', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('clients/create', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),
    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('messages/create', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),
    path('newsletters/report', NewsletterTryListView.as_view(), name='newsletters_report'),
]
