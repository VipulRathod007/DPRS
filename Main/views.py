from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import send_mail


context = {
    "title": "DPRS",
    "author": "The Avengers",
    "contact": "+12 7578665",
    "mail": "info@dprs.com",
    "address": "Hi-Tech City, Bengalore, India"
}


def home(request):
    return render(request, 'Main/index.html', context=context)


def about(request):
    return render(request, 'Main/about.html', context=context)


def contact(request):
    context["message"] = ''
    if request.method == 'POST':
        name = request.POST["name"]
        mail = request.POST["mail"]
        subject = request.POST["subject"]
        message = request.POST["message"]
        send_mail(subject + " from " + name, message, mail,
                  ["vipuldrathod1458@gmail.com"])
        context['message'] = "Mail Sent Succesfully!"
        return render(request, 'Main/contact.html', context=context)
    else:
        return render(request, 'Main/contact.html', context=context)
