from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import WarehouseUser
from .forms import WarehouseUserChangeForm, RegisterForm


User = get_user_model()


class WarehouseUserAdmin(UserAdmin):
    """Forms to add and change user instances"""
    form = WarehouseUserChangeForm
    add_form = RegisterForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'admin')
    list_filter = ('admin', 'staff')
    fieldsets = (
        ('User Info', {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('date_of_birth', 'phone_number', 'gender', 'employee_id')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth',
                       'gender', 'phone_number', 'employee_id', 'password1',
                       'password2', 'admin', 'staff', 'active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Register the WarehouseUser
admin.site.register(WarehouseUser, WarehouseUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
