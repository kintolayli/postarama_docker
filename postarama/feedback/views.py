from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render

from yatube import settings
from .forms import FeedbackForm


def feedback(request):
    form = FeedbackForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():

            email_subject = 'POSTARAMA :: Сообщение через контактную форму '
            email_body = "С сайта отправлено новое сообщение\n\n" \
                         "Имя отправителя: %s \n" \
                         "E-mail отправителя: %s \n\n" \
                         "Сообщение: \n" \
                         "%s " % \
                         (form.cleaned_data['name'],
                          form.cleaned_data['email'],
                          form.cleaned_data['message'])

            # отправляем сообщение
            try:
                send_mail(email_subject, email_body,
                          settings.EMAIL_HOST_USER,
                          settings.EMAIL_TO, fail_silently=False)
                messages.success(request, 'Сообщение отправлено успешно')
            except Exception as e:
                messages.error(request, 'Что-то пошло не так =(')
                # TODO: добавить сюда логирование

        form = FeedbackForm()
        return render(request, 'feedback.html', context={'form': form})

    return render(request, 'feedback.html', context={'form': form})
