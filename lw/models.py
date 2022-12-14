from django.db import models
from django.conf import settings
# Create your models here.
# Helpful django migration info
# https://realpython.com/django-migrations-a-primer/#creating-migrations


class Search(models.Model):
    """Search. References user's id"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20)
    url = models.CharField(max_length=50)
    elemtype = models.CharField(max_length=50, default='', blank=True)
    elemattr = models.CharField(max_length=100, default='', blank=True)
    dateCreated = models.DateField(auto_now_add=True)
    state = models.BooleanField(default=True)


class Result(models.Model):
    """Result. References search id"""

    sourceSearch = models.ForeignKey(Search, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, default="EMPTY URL")
    sent = models.BooleanField(default=False)
    sample = models.TextField(default="")
