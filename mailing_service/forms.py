from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField
from mailing_service.models import Client, Message, Newsletter


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ClientForm(FormStyleMixin, ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(FormStyleMixin, ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class NewsletterForm(FormStyleMixin, ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'
