from django.db import models


class User(models.Model):
    email = models.EmailField()
    passwd = models.CharField(max_length=50)

    def __str__(self):
        return self.email
