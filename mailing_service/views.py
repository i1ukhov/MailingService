from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView

from mailing_service.models import Newsletter, Client, Message, NewsletterTry

from mailing_service.forms import ClientForm, MessageForm, NewsletterForm, NewsletterModeratorForm


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('mailing_service:newsletters_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return NewsletterForm
        elif user.has_perm('mailing_service.can_block_newsletters'):
            return NewsletterModeratorForm
        else:
            raise PermissionDenied


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('mailing_service:newsletters_list')


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('mailing_service:newsletters_list')

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.owner = user
        newsletter.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:clients_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:clients_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_service:clients_list')


class Homepage(TemplateView):
    template_name = 'mailing_service/index.html'


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:messages_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:messages_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_service:messages_list')


class NewsletterTryListView(LoginRequiredMixin, ListView):
    model = NewsletterTry

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['total'] = NewsletterTry.objects.all()
        context_data['total_count'] = NewsletterTry.objects.all().count()
        context_data['successful_count'] = NewsletterTry.objects.filter(success=True).count()
        context_data['unsuccessful_count'] = NewsletterTry.objects.filter(success=False).count()
        return context_data
