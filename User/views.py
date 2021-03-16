from django.shortcuts import render, redirect
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
        if User.objects.filter(email=mail).first() is None:
            tempUser = User()
            tempUser.email = mail
            tempUser.passwd = passwd
            tempUser.save()
            request.session['current-user'] = tempUser.email
            context['user'] = tempUser
            context['tabTitle'] = 'Home'
            messages.success(request, f"New account created: {User.objects.filter(email=mail).first().id}")
            return render(request, 'Main/index.html', context=context)
        else:
            context['user'] = None
            context['tabTitle'] = 'Register'
            messages.success(request, f"Account already exists!")
            return render(request, 'User/Register.html', context=context)
    elif request.method == "GET":
        return render(request, 'User/Register.html', context=context)


def login(request):
    context['tabTitle'] = "Login"
    if request.method == "GET":
        if 'current-user' in request.session:
            return redirect("/")
        else:
            return render(request, 'User/Login.html', context=context)
    elif request.method == "POST":
        id = request.POST['id']
        passwd = request.POST['pass']

        matchUser = User.objects.filter(email=id).first()
        if matchUser is not None and matchUser.passwd == passwd:
            request.session['current-user'] = id
            context['user'] = matchUser
            context['tabTitle'] = 'Home'
            return render(request, 'Main/index.html', context=context)
        else:
            return redirect("/user/login/")


def logout(request):
    context['tabTitle'] = "Home"
    request.session.pop('current-user')
    context['user'] = None
    context['tabTitle'] = 'Home'
    return render(request, 'Main/index.html', context=context)


def profile(request):
    if "current-user" in request.session and context['user'] is not None:
        return render(request, 'User/Profile.html', context=context)
    else:
        return redirect("/user/login/")
