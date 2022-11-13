from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Search, Result#, User

admin.site.register(Search)
admin.site.register(Result)
#admin.site.register(User, UserAdmin)