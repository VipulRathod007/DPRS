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
