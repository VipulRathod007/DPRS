from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import json
from datetime import datetime
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


def hospitalRegister(request):
    context['tabTitle'] = "Hospital Registration"
    if request.method == "POST":
        mail = request.POST['email']
        passwd = request.POST['pass']
        if Hospital.objects.filter(email=mail).first() is None:
            tempUser = Hospital()
            tempUser.email = mail
            tempUser.passwd = passwd
            tempUser.basicFlag = False
            tempUser.save()
            request.session['current-user'] = Hospital.objects.filter(email=mail).first().id
            context['user'] = tempUser
            messages.success(request, f"New Hospital account created: {Hospital.objects.filter(email=mail).first().email}")
            return redirect(context['appUsers']['profile']['Hospitals'])
        else:
            context['user'] = None
            context['tabTitle'] = "Hospital Registration"
            messages.success(request, f"Hospital Account already exists!")
            return redirect(context['appUsers']['register']['Hospitals'])
    elif request.method == "GET":
        if 'current-user' in request.session:
            return redirect(context['appUsers']['profile']['Hospitals'])
        else:
            return render(request, 'User/Register.html', context=context)


def ngoRegister(request):
    context['tabTitle'] = "NGO Registration"
    if request.method == "POST":
        mail = request.POST['email']
        passwd = request.POST['pass']
        if NGO.objects.filter(email=mail).first() is None:
            tempUser = NGO()
            tempUser.email = mail
            tempUser.passwd = passwd
            tempUser.basicFlag = False
            tempUser.save()
            request.session['current-user'] = NGO.objects.filter(email=mail).first().id
            context['user'] = tempUser
            messages.success(request, f"New NGO account created: {NGO.objects.filter(email=mail).first().email}")
            return redirect(context['appUsers']['profile']['NGOs'])
        else:
            context['user'] = None
            context['tabTitle'] = "NGO Registration"
            messages.success(request, f"NGO Account already exists!")
            return redirect(context['appUsers']['register']['NGOs'])
    elif request.method == "GET":
        if 'current-user' in request.session:
            return redirect(context['appUsers']['profile']['NGOs'])
        else:
            return render(request, 'User/Register.html', context=context)


def login(request):
    context['tabTitle'] = "Login"
    if request.method == "GET":
        if 'current-user' in request.session:
            return redirect(context['appUsers']['profile'][context['selectedTypeUser']])
        else:
            return render(request, 'User/Login.html', context=context)
    elif request.method == "POST":
        mail = request.POST['email']
        passwd = request.POST['pass']
        if context['selectedTypeUser'] == 'Users':
            matchUser = User.objects.filter(email=mail).first()
        elif context['selectedTypeUser'] == 'Hospitals':
            matchUser = Hospital.objects.filter(email=mail).first()
        elif context['selectedTypeUser'] == 'NGOs':
            matchUser = NGO.objects.filter(email=mail).first()

        if matchUser is not None and matchUser.passwd == passwd:
            request.session['current-user'] = matchUser.id
            context['user'] = matchUser
            context['tabTitle'] = 'Home'
            return redirect(context['appUsers']['profile'][context['selectedTypeUser']])
        else:
            messages.warning(request, f"Invalid Credentials!")
            return redirect(context['appUsers']['login']['Users'])


def showPatients(request):
    if 'current-user' in request.session and context['selectedTypeUser'] == "Hospitals":
        context['tabTitle'] = "Admitted Patients"
        admissions = Admission.objects.filter(hospitalid=request.session['current-user'])
        context['admissions'] = admissions
        return render(request, "User/ShowPatients.html", context=context)
    else:
        messages.warning(request, f"Invalid Credentials!")
        return redirect(context['appUsers']['login']['Users'])


def dischargePatient(request):
    pid = ""
    if 'current-user' in request.session and context['selectedTypeUser'] == 'Hospitals':
        context['tabTitle'] = "Discharge Patient"
        if request.method == 'POST':
            # if pid == "":
            admissionObj = Admission.objects.filter(id=context['admission-id']).first()
            # else:
            #     admissionObj = Admission.objects.filter(id=pid).first()
            admissionObj.cause = request.POST['cause']
            admissionObj.prescription = request.POST['prescription']
            admissionObj.billamt = float(request.POST['billamt'])
            fs = FileSystemStorage()
            bill = request.FILES['bill']
            billFileName = fs.save("Reports" + str(admissionObj.id) + bill.name, bill)
            admissionObj.bill = ".." + fs.url(billFileName)
            admissionObj.dischargeDate = datetime.now()
            admissionObj.save()
            request.session.pop('patient-id')
            messages.success(request, f"Discharged Successfully!")
            return redirect("/user/showPatients/")
        elif request.method == 'GET':
            if 'id' in request.GET:
                pid = request.GET['id']
                context['admission-id'] = pid
                admissionObj = Admission.objects.filter(id=pid).first()
                context['patient'] = User.objects.filter(id=admissionObj.patientid).first()
                context['admissionDetails'] = admissionObj
                request.session['patient-id'] = context['patient'].id
            allPatients = Admission.objects.filter(hospitalid=request.session['current-user'])
            admittedPatients = []
            for admittedPatient in allPatients:
                if admittedPatient.dischargeDate == "":
                    admittedPatients.append(admittedPatient)
            context['admittedPatients'] = admittedPatients
            return render(request, "User/DischargePatient.html", context=context)
    else:
        return redirect("/")


def admissionHistory(request):
    if 'current-user' in request.session and context['selectedTypeUser'] == "Users":
        context['tabTitle'] = "Hospital Admission History"
        admissions = Admission.objects.filter(patientid=request.session['current-user'])
        # hospitalDetails = []
        # for admission in admissions:
        #     hospitalDetails.append(Hospital.objects.filter(id=admission.hospitalid).first())
        context['admissions'] = admissions
        return render(request, "User/AdmissionHistory.html", context=context)
    else:
        messages.warning(request, f"Access Denied!")
        return redirect(context['appUsers']['login']['Users'])


def logout(request):
    if 'current-user' in request.session:
        context['tabTitle'] = "Home"
        request.session.pop('current-user')
        context['user'] = None
        context['selectedTypeUser'] = None
        context['editFlag'] = False
        messages.success(request, f"Logged Out Successfully!")
        return redirect("/")
    else:
        return redirect("/")


def admitPatient(request):
    if 'current-user' in request.session and context['selectedTypeUser'] == 'Hospitals':
        context['tabTitle'] = "Admit Patient"
        if request.method == 'POST':
            fs = FileSystemStorage()
            healthid = request.session['patient-id']
            cause = request.POST['cause']
            report = request.FILES['reports']
            prescription = request.POST['prescription']
            userObj = User.objects.filter(healthid=healthid).first()
            hospitalObj = Hospital.objects.filter(id=request.session['current-user']).first()
            reportFileName = fs.save("Reports" + str(userObj.id) + report.name, report)
            admissionObj = Admission()
            admissionObj.cause = cause
            admissionObj.patientid = userObj.id
            admissionObj.hospitalid = hospitalObj.id
            admissionObj.prescription = prescription
            admissionObj.report = ".." + fs.url(reportFileName)
            admissionObj.patientname = userObj.fname + ' ' + userObj.lname
            admissionObj.admitDate = datetime.now()
            admissionObj.hospitalname = hospitalObj.name
            admissionObj.save()
            messages.success(request, 'Patient admitted Successfully!')
            return redirect('/user/showPatients/')
        elif request.method == 'GET':
            return render(request, 'User/AdmitPatient.html', context=context)
    else:
        context['selectedTypeUser'] = 'Hospitals'
        messages.warning(request, 'Login first to access the page!')
        return redirect(context['appUsers']['login']['Hospitals'])


def patientSearch(request):
    if 'current-user' in request.session and context['selectedTypeUser'] == 'Hospitals':
        context['tabTitle'] = "Admit Patient"
        if request.method == 'POST':
            redirectLoc = int(request.POST['redirectUrl'])
            if 'healthid' in request.POST:
                healthid = request.POST['healthid']
                try:
                    request.session['patient-id'] = int(healthid)
                    context['patient'] = User.objects.filter(healthid=healthid).first()
                except:
                    messages.warning(request, 'Enter Valid Health ID!')
                    return redirect(context['appUsers']['login']['Hospitals'])
                if redirectLoc == 1:
                    return redirect('/user/dischargePatient/')
            elif 'admissionid' in request.POST:
                admissionid = request.POST['admissionid']
                context['patient'] = User.objects.filter(id=Admission.objects.filter(id=admissionid).first().patientid).first()
                if redirectLoc == 1:
                    url = '/user/dischargePatient/?id=' + str(admissionid)
                    return redirect(url)
            if redirectLoc == 0:
                return redirect('/user/admitPatient/')
        elif request.method == 'GET':
            messages.warning(request, 'Access Denied!')
            return redirect('/')
    else:
        context['selectedTypeUser'] = 'Hospitals'
        messages.warning(request, 'Login first to access the page!')
        return redirect(context['appUsers']['login']['Hospitals'])


def registerChoice(request):
    if request.method == "POST":
        choice = request.POST['typeUser']
        if choice == '-1':
            messages.warning(request, "Please Select User Type for Registration!")
            context['selectedTypeUser'] = choice
            return redirect(context['appUsers']['register']['Users'])
        else:
            context['selectedTypeUser'] = choice
            return redirect(context['appUsers']['register'][choice])
    else:
        messages.warning(request, "Invalid Operation!")
        return redirect(context['appUsers']['register']['Users'])


def loginChoice(request):
    if request.method == "POST":
        choice = request.POST['typeUser']
        if choice == '-1':
            messages.warning(request, "Please Select User Type for Registration!")
            context['selectedTypeUser'] = choice
            return redirect(context['appUsers']['login']['Users'])
        else:
            context['selectedTypeUser'] = choice
            return redirect(context['appUsers']['login'][choice])
    else:
        messages.warning(request, "Invalid Operation!")
        return redirect(context['appUsers']['login']['Users'])


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
        if User.objects.filter(id=request.session['current-user']).first() is not None:
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
        if User.objects.filter(id=request.session['current-user']).first() is not None:
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
        if context['selectedTypeUser'] == 'Users':
            userObj = User.objects.filter(id=request.session['current-user']).first()
        elif context['selectedTypeUser'] == 'Hospitals':
            userObj = Hospital.objects.filter(id=request.session['current-user']).first()
        elif context['selectedTypeUser'] == 'NGOs':
            userObj = NGO.objects.filter(id=request.session['current-user']).first()

        userObj.basicFlag = False
        userObj.save()
        return redirect(context['appUsers']['profile'][context['selectedTypeUser']])
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
            if context['selectedTypeUser'] == 'Users':
                context['user'] = User.objects.filter(id=request.session['current-user']).first()
                return render(request, 'User/Profile.html', context=context)
            elif context['selectedTypeUser'] == 'Hospitals':
                context['user'] = Hospital.objects.filter(id=request.session['current-user']).first()
                return render(request, 'User/HospitalProfile.html', context=context)
            elif context['selectedTypeUser'] == 'NGOs':
                context['user'] = NGO.objects.filter(id=request.session['current-user']).first()
                return render(request, 'User/NGOProfile.html', context=context)
        else:
            messages.warning(request, f"Login to check Profile Page!")
            return redirect(context['appUsers']['login']['Users'])
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
                    return redirect(context['appUsers']['profile']['Users'])
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
            userObj.healthid = aadhar
            userObj.gender = gender
            userObj.contact = contact
            userObj.aadhar = aadhar
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
            userObj.save()
            flag = None
            messages.success(request, f"Your details saved successfully!")
            return redirect(context['appUsers']['profile']['Users'])


def hospitalProfile(request):
    flag = None
    global editFlag
    if 'editFlag' in context and context['editFlag']:
        context['tabTitle'] = "Edit Hospital Profile"
    else:
        context['tabTitle'] = "Hospital Profile"
    if request.method == 'GET':
        if "current-user" in request.session:
            context['user'] = Hospital.objects.filter(id=request.session['current-user']).first()
            return render(request, 'User/HospitalProfile.html', context=context)
        else:
            messages.warning(request, f"Login to check Hospital Profile Page!")
            return redirect(context['appUsers']['login']['Hospitals'])
    elif request.method == 'POST' and "current-user" in request.session:
        userObj = Hospital.objects.filter(id=request.session['current-user']).first()
        if not userObj.basicFlag:
            name = request.POST['name']
            contact = request.POST['contact']
            website = request.POST['website']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            zipCode = request.POST['zipcode']
            mediclaim = request.POST['mediclaim']
            hospitalType = request.POST['hospitalType']
            hospitalSpec = request.POST['hospitalSpec']
            userObj.name = name
            userObj.contact = contact
            userObj.website = website
            userObj.address = address1 + " " + address2
            userObj.city = city
            userObj.state = state
            userObj.country = country
            userObj.zipcode = zipCode
            userObj.basicFlag = True
            userObj.mediclaim = mediclaim
            userObj.hospitalType = hospitalType
            userObj.hospitalSpec = hospitalSpec
            userObj.save()
            flag = None
            messages.success(request, f"Your details saved successfully!")
            return redirect(context['appUsers']['profile']['Hospitals'])


def ngoProfile(request):
    flag = None
    global editFlag
    if 'editFlag' in context and context['editFlag']:
        context['tabTitle'] = "Edit NGO Profile"
    else:
        context['tabTitle'] = "NGO Profile"
    if request.method == 'GET':
        if "current-user" in request.session:
            context['user'] = NGO.objects.filter(id=request.session['current-user']).first()
            return render(request, 'User/NGOProfile.html', context=context)
        else:
            messages.warning(request, f"Login to check NGO Profile Page!")
            return redirect(context['appUsers']['login']['NGOs'])
    elif request.method == 'POST' and "current-user" in request.session:
        userObj = NGO.objects.filter(id=request.session['current-user']).first()
        if not userObj.basicFlag:
            name = request.POST['name']
            contact = request.POST['contact']
            website = request.POST['website']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            zipCode = request.POST['zipcode']
            userObj.name = name
            userObj.contact = contact
            userObj.website = website
            userObj.address = address1 + " " + address2
            userObj.city = city
            userObj.state = state
            userObj.country = country
            userObj.zipcode = zipCode
            userObj.basicFlag = True
            userObj.save()
            flag = None
            messages.success(request, f"Your details saved successfully!")
            return redirect(context['appUsers']['profile']['NGOs'])
