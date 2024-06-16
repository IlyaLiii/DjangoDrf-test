from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import HttpResponse

from feedback.forms import ContactForm
from feedback.models import Contact
from services.email import send_contact_email_message


class ContactCreate(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'feedback/contact_form.html'
    extra_context = {'title': 'Контактная форма'}
    success_url = reverse_lazy('success_page')
    success_message = 'Ваше письмо успешно отправлено администрации сайта'

    def form_valid(self, form):
        if form.is_valid():
            data = form.data
            sender = data['email']
            subject = f'Сообщение с формы от {data["username"]} Почта отправителя: {sender}'

        send_contact_email_message(subject, data['message'], sender)
        return super().form_valid(form)


def success(request):
    return HttpResponse('Письмо отправлено!')
