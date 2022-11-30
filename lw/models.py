from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.
# Helpful django migration info
# https://realpython.com/django-migrations-a-primer/#creating-migrations
"""
class User(AbstractUser):
    pass
"""


class Search(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20)
    url = models.CharField(max_length=50)
    elemtype = models.CharField(max_length=50)
    elemattr = models.CharField(max_length=100)
    dateCreated = models.DateField(auto_now_add=True)
    state = models.BooleanField(default=True)


class Result(models.Model):
    sourceSearch = models.ForeignKey(Search, on_delete=models.CASCADE)
    url = models.CharField(max_length = 255, default="EMPTY URL") # This is the specific url where the keyword was found
    sent = models.BooleanField(default=False) # Can be used to mark whether a result has been sent to the user
    sample = models.TextField(default="")
