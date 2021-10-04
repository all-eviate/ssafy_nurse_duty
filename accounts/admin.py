from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm,UserChangeForm
from .models import User

# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('pk', 'username', 'name', 'birth','started_working','team','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None,{'fields':('username','password')}),
        ("Personal info",{'fields':('name', 'birth','started_working','team')}),
        ("Permissions",{'fields':('is_admin',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','name', 'birth','started_working','team', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)