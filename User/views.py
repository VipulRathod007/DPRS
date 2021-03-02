from django.shortcuts import render
from .models import User
from django.contrib import messages


context = {
    "title": "DPRS",
    "author": "The Avengers",
    "contact": "+12 7578665",
    "mail": "info@dprs.com",
    "address": "Hi-Tech City, Bengalore, India"
}


def register(request):
    context['tabTitle'] = "Register"
    if request.method == "POST":
        mail = request.POST['email']
        passwd = request.POST['pass']
        # flag = request.POST['remember']
        # if flag:
        #     pass
        tempUser = User()
        tempUser.email = mail
        tempUser.passwd = passwd
        tempUser.save()
        messages.success(request, f"New account created: {mail}")
    elif request.method == "GET":
        return render(request, 'User/Register.html', context=context)


def login(request):
    context['tabTitle'] = "Login"
    return render(request, 'User/Login.html', context=context)


