from django.contrib import admin
from .models import User, Profile
from import_export.admin import ImportExportModelAdmin


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display= ["id", "username", "email"]


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    list_display= [field.name for field in Profile._meta.fields]

    
