from django.contrib import admin
from .models import Nurse

# Register your models here.
class NurseAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Nurse)