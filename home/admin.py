from django.contrib import admin

# Register your models here.

from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','age','gender','description','photo','resume')
    fields = ['user','age','gender','description','photo','resume']

# Register the admin class with the associated model
admin.site.register(Profile, ProfileAdmin)
