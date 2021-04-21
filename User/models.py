from django.db import models


class User(models.Model):
    email = models.EmailField()
    passwd = models.CharField(max_length=50)
    fname = models.CharField(max_length=50, default="")
    healthid = models.CharField(max_length=50, default="")
    lname = models.CharField(max_length=50, default="")
    dob = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=15, default="")
    contact = models.CharField(max_length=15, default="")
    aadhar = models.CharField(max_length=25, default="")
    aadharPic = models.CharField(max_length=250, default="")
    profilePic = models.CharField(max_length=250, default="")
    address = models.CharField(max_length=350, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    zipcode = models.CharField(max_length=20, default="")
    basicFlag = models.BooleanField()

    def __str__(self):
        if self.fname == "":
            return self.email
        else:
            return self.fname


class Admission(models.Model):
    patientid = models.IntegerField(max_length=50)
    patientname = models.CharField(max_length=50, default="")
    hospitalname = models.CharField(max_length=150, default="")
    cause = models.CharField(max_length=250, default="")
    report = models.CharField(max_length=250, default="")
    bill = models.CharField(max_length=250, default="")
    billamt = models.FloatField(max_length=10, default=0)
    prescription = models.CharField(max_length=2250, default="")
    billpaid = models.BooleanField(default=False)
    pendingbillamt = models.FloatField(default=0)
    admitDate = models.CharField(max_length=100, default="")
    dischargeDate = models.CharField(max_length=100, default="")
    hospitalid = models.IntegerField(max_length=50)

    def __str__(self):
        return str(self.patientname) + ' admitted in ' + str(self.hospitalname) + ' on ' + str(self.admitDate)


class Hospital(models.Model):
    email = models.EmailField()
    passwd = models.CharField(max_length=50)
    name = models.CharField(max_length=50, default="")
    hospitalid = models.CharField(max_length=50, default="")
    contact = models.CharField(max_length=15, default="")
    website = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=350, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    zipcode = models.CharField(max_length=20, default="")
    basicFlag = models.BooleanField()
    isGranted = models.BooleanField(null=True)
    hospitalType = models.CharField(max_length=100, default="")
    hospitalSpec = models.CharField(max_length=150, default="")

    def __str__(self):
        if self.name == "":
            return "Hospital - " + str(self.email)
        else:
            return self.name


class NGO(models.Model):
    email = models.EmailField()
    passwd = models.CharField(max_length=50)
    name = models.CharField(max_length=50, default="")
    ngoid = models.CharField(max_length=50, default="")
    contact = models.CharField(max_length=15, default="")
    website = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=350, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    zipcode = models.CharField(max_length=20, default="")
    basicFlag = models.BooleanField()

    def __str__(self):
        if self.name == "":
            return "NGO - " + str(self.email)
        else:
            return self.name


class Bill(models.Model):
    admissionid = models.IntegerField()
    billamt = models.FloatField(max_length=10, default=0)
    billpaid = models.BooleanField(default=False)
    pendingbillamt = models.FloatField(default=0)
    billImg = models.CharField(max_length=250, default="")
    timeofBillAddition = models.CharField(max_length=50, default="")
    billDesc = models.CharField(max_length=350, default="")

    def __str__(self):
        return "Bill of " + str(self.billamt) + " Rs"


class HelpRequest(models.Model):
    patientid = models.IntegerField()
    hospitalid = models.IntegerField()
    ngoid = models.IntegerField()
    ngoname = models.CharField(max_length=250, default="")
    admissionid = models.IntegerField()
    isapproved = models.BooleanField(null=True)
    approvedamt = models.FloatField(default=0)
    requestedamt = models.FloatField()
    requestdate = models.CharField(max_length=25, default="")
    responsedate = models.CharField(max_length=25, default="")
