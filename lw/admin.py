from django.contrib import admin

# Register your models here.
from .models import Search, Result

admin.site.register(Search)
admin.site.register(Result)
