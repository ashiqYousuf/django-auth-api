from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserModelAdmin(BaseUserAdmin):

    list_display = ('id', 'email', 'name' , 'tc' , 'is_admin' , 'created_at' , 'updated_at')
    list_filter = ('is_admin',)
    # Managing the UI
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','tc')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # Fields to show up when creating a User
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','tc', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
