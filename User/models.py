from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    passwd = models.TextField()
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
