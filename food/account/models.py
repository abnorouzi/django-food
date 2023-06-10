from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logo/')
    avatar = models.ImageField(upload_to='avatar/', null=True)
    tel = models.CharField(max_length=11)
    address = models.TextField(null=True)
    company = models.CharField(max_length=50)
    cat = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user) + " Account"
