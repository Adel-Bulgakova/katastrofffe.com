# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import ContactForm
from django.utils import timezone

from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from constance import config


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.published_date = timezone.now()
            contact.save()

            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject, from_email, to = 'Message from katastrofffe.com', 'contact@katastrofffe.com', config.CONTACT_EMAIL

            html_content = render_to_string('contact/mail_template.html', {'message': message, 'email': email})
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")

            try:
                msg.send()
                status = 'OK'
                system_message = 'Thank you! Your message has been sent.'
                return render(request, 'contact/contact.html', {'form': form, 'status': status, 'system_message': system_message})

            except SMTPException:
                status = 'ERROR'
                system_message = "Sorry! Something went wrong, your message hasn't been sent."
                return render(request, 'contact/contact.html', {'form': form, 'status': status, 'system_message': system_message})

    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})
