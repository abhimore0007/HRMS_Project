from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import  Leave, LeaveQuota

admin.site.register(Leave)
admin.site.register(LeaveQuota)
