from django.contrib import admin
from .models import NewUser
# Register your models here.


@admin.register(NewUser)
class AdminNewUser(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name','last_name',
    ]