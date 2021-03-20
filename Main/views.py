from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import send_mail
import json

with open('config.json', 'r') as file:
    jsonFile = json.load(file)
    context = jsonFile['context']


def home(request):
    context['tabTitle'] = "Home"
    return render(request, 'Main/index.html', context=context)


def about(request):
    context['tabTitle'] = "About"
    return render(request, 'Main/about.html', context=context)


def contact(request):
    context['tabTitle'] = "Contact"
    context["message"] = ''
    if request.method == 'POST':
        name = request.POST["name"]
        mail = request.POST["mail"]
        subject = request.POST["subject"]
        message = request.POST["message"]
        send_mail(subject + " from " + name, message, mail,
                  ["contact.dprs.web@gmail.com"])
        context['message'] = "Mail Sent Succesfully!"
        return render(request, 'Main/contact.html', context=context)
    else:
        return render(request, 'Main/contact.html', context=context)
