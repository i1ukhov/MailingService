from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView

from mailing_service.models import Newsletter, Client, Message, NewsletterTry

from mailing_service.forms import ClientForm, MessageForm, NewsletterForm


class NewsletterListView(ListView):
    model = Newsletter


class NewsletterDetailView(DetailView):
    model = Newsletter


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('mailing_service:newsletters_list')


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('mailing_service:newsletters_list')


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('mailing_service:newsletters_list')


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:clients_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:clients_list')


class ClientListView(ListView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_service:clients_list')


class Homepage(TemplateView):
    template_name = 'mailing_service/index.html'


class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:messages_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:messages_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_service:messages_list')


class NewsletterTryListView(ListView):
    model = NewsletterTry

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['total'] = NewsletterTry.objects.all()
        context_data['total_count'] = NewsletterTry.objects.all().count()
        context_data['successful_count'] = NewsletterTry.objects.filter(success=True).count()
        context_data['unsuccessful_count'] = NewsletterTry.objects.filter(success=False).count()
        return context_data
