from django.db import models


class User(models.Model):
    email = models.EmailField()
    passwd = models.CharField(max_length=50)
    fname = models.CharField(max_length=50, default="")
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
