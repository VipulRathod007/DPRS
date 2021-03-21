from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import json
import os
from django.core.files.storage import FileSystemStorage

with open('config.json', 'r') as file:
    jsonFile = json.load(file)
    context = jsonFile['context']


editFlag = False


def register(request):
    context['tabTitle'] = "Register"
    if request.method == "POST":
        mail = request.POST['email']
        passwd = request.POST['pass']
        if User.objects.filter(email=mail).first() is None:
            tempUser = User()
            tempUser.email = mail
            tempUser.passwd = passwd
            tempUser.basicFlag = False
            tempUser.save()
            request.session['current-user'] = User.objects.filter(email=mail).first().id
            context['user'] = tempUser
            context['tabTitle'] = 'Home'
            messages.success(request, f"New account created: {User.objects.filter(email=mail).first().email}")
            return redirect("/user/profile/")
        else:
            context['user'] = None
            context['tabTitle'] = 'Register'
            messages.success(request, f"Account already exists!")
            return redirect("/user/register/")
    elif request.method == "GET":
        if 'current-user' in request.session:
            return redirect("/user/profile/")
        else:
            return render(request, 'User/Register.html', context=context)


def login(request):
    context['tabTitle'] = "Login"
    if request.method == "GET":
        if 'current-user' in request.session:
            return redirect("/user/profile/")
        else:
            return render(request, 'User/Login.html', context=context)
    elif request.method == "POST":
        mail = request.POST['email']
        passwd = request.POST['pass']
        matchUser = User.objects.filter(email=mail).first()
        if matchUser is not None and matchUser.passwd == passwd:
            request.session['current-user'] = matchUser.id
            context['user'] = matchUser
            context['tabTitle'] = 'Home'
            return redirect("/user/profile/")
        else:
            messages.warning(request, f"Invalid Credentials!")
            return redirect("/user/login/")


def logout(request):
    if 'current-user' in request.session:
        context['tabTitle'] = "Home"
        request.session.pop('current-user')
        context['user'] = None
        context['editFlag'] = False
        messages.success(request, f"Logged Out Successfully!")
        return redirect("/")
    else:
        return redirect("/")


def profileEdit(request):
    if 'current-user' in request.session:
        context['tabTitle'] = "Edit Profile"
        context['editFlag'] = True
        global editFlag
        editFlag = True
        userObj = User.objects.filter(id=request.session['current-user']).first()
        userObj.basicFlag = False
        userObj.save()
        return redirect("/user/profile/")
    else:
        return redirect("/")


def profilePicEdit(request):
    if 'current-user' in request.session:
        if User.objects.filter(id=request.session['current-user']).first().basicFlag:
            if request.method == "GET":
                context['tabTitle'] = "Edit Profile Picture"
                context['user'] = User.objects.filter(id=request.session['current-user']).first()
                return render(request, "User/EditProfilePic.html", context=context)
            elif request.method == "POST":
                fs = FileSystemStorage()
                userObj = User.objects.filter(id=request.session['current-user']).first()
                profilePic = request.FILES['profilePic']
                profilePicName = fs.save("PicP" + str(userObj.id) + profilePic.name, profilePic)
                userObj.profilePic = ".." + fs.url(profilePicName)
                userObj.save()
                messages.success(request, f"New Profile Picture saved successfully!")
                return redirect("/user/profile/")
        else:
            return redirect("/user/profile/")
    else:
        return redirect("/user/login/")


def aadharPicEdit(request):
    if 'current-user' in request.session:
        if User.objects.filter(id=request.session['current-user']).first().basicFlag:
            if request.method == "GET":
                context['tabTitle'] = "Edit Aadhar Copy"
                context['user'] = User.objects.filter(id=request.session['current-user']).first()
                return render(request, "User/EditAadharPic.html", context=context)
            elif request.method == "POST":
                fs = FileSystemStorage()
                userObj = User.objects.filter(id=request.session['current-user']).first()
                aadharPic = request.FILES['aadharPic']
                aadharPicName = fs.save("PicA" + str(userObj.id) + aadharPic.name, aadharPic)
                userObj.aadharPic = ".." + fs.url(aadharPicName)
                userObj.save()
                messages.success(request, f"New Aadhar Copy saved successfully!")
                return redirect("/user/profile/")
        else:
            return redirect("/user/profile/")
    else:
        return redirect("/user/login/")


def profileEdit(request):
    if 'current-user' in request.session:
        context['tabTitle'] = "Edit Profile"
        context['editFlag'] = True
        global editFlag
        editFlag = True
        userObj = User.objects.filter(id=request.session['current-user']).first()
        userObj.basicFlag = False
        userObj.save()
        return redirect("/user/profile/")
    else:
        return redirect("/")


def profile(request):
    flag = None
    global editFlag
    if 'editFlag' in context and context['editFlag']:
        context['tabTitle'] = "Edit Profile"
    else:
        context['tabTitle'] = "Profile"
    if request.method == 'GET':
        if "current-user" in request.session:
            context['user'] = User.objects.filter(id=request.session['current-user']).first()
            return render(request, 'User/Profile.html', context=context)
        else:
            messages.warning(request, f"Login to check Profile Page!")
            return redirect("/user/login/")
    elif request.method == 'POST' and "current-user" in request.session:
        userObj = User.objects.filter(id=request.session['current-user']).first()
        if not userObj.basicFlag:
            fs = FileSystemStorage()
            fname = request.POST['fname']
            lname = request.POST['lname']
            dob = request.POST['dob']
            gender = request.POST['gender']
            contact = request.POST['contact']
            aadhar = request.POST['aadhar']
            try:
                aadharPic = request.FILES['aadharPic']
                profilePic = request.FILES['profilePic']
            except:
                if userObj.fname == "":
                    messages.success(request, f"Upload Profile picture and Aadhar Card Copy.")
                    return redirect("/user/profile/")
                else:
                    flag = True
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            zipCode = request.POST['zipcode']
            userObj.fname = fname
            userObj.lname = lname
            userObj.dob = dob
            userObj.gender = gender
            userObj.contact = contact
            userObj.aadhar = aadhar
            # userObj.aadharPic = "PicA" + str(userObj.id) + aadharPic.name
            # userObj.profilePic = "PicP" + str(userObj.id) + profilePic.name
            if not flag:
                aadharPicName = fs.save("PicA" + str(userObj.id) + aadharPic.name, aadharPic)
                profilePicName = fs.save("PicP" + str(userObj.id) + profilePic.name, profilePic)
                userObj.aadharPic = ".." + fs.url(aadharPicName)
                userObj.profilePic = ".." + fs.url(profilePicName)
            userObj.address = address1 + " " + address2
            userObj.city = city
            userObj.state = state
            userObj.country = country
            userObj.zipcode = zipCode
            userObj.basicFlag = True
            # aadharPic.save(os.path.join(context['uploadTo'], userObj.aadharPic))
            # profilePic.save(os.path.join(context['uploadTo'], userObj.profilePic))
            userObj.save()
            flag = None
            messages.success(request, f"Your details saved successfully!")
            return redirect("/user/profile/")
