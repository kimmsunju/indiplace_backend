from django.db import models

class Member(models.Model):
    loginid = models.CharField(max_length=10)
    loginpw = models.CharField(max_length=15)
