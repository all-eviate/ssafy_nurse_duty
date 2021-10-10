from django.contrib import admin
from .models import Nurse, Team

class NurseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'choices',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'team',)


admin.site.register(Nurse, NurseAdmin)
admin.site.register(Team, TeamAdmin)
