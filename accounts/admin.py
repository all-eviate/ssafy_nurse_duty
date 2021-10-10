from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'user_id', 'name', 'emp_id', 'emp_team', 'emp_grade', 'is_admin'
    )
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        ('Personal info', {'fields': ('name', 'emp_id', 'emp_team', 'emp_grade',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute.
    # UserAdmin overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'name', 'emp_id', 'emp_team', 'emp_grade', 'password1', 'password2'),
        }),
    )
    search_fields = ('user_id',)
    ordering = ('user_id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
# since we're not using Django's built-in permissions, unregister the Group model from admin.
admin.site.unregister(Group)
