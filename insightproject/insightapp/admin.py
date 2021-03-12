from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Profile, Asiointi, Ruokalista, RavinVaikutu, Perustiedot


# Register your models here.
#current user
User = get_user_model()


#user admin
class UserAdmin(BaseUserAdmin):
    """form = UserAdminChangeForm
    add_form = UserAdminCreationForm"""

    list_display = ('email','fname', 'lname', 'admin',)
    list_filter = ('staff', 'active', 'admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('fname', 'lname', 'score',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

    search_fields = ('email', 'fname', 'lname')
    ordering = ('email', 'fname')
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


#register my models
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Asiointi)
admin.site.register(Ruokalista)
admin.site.register(RavinVaikutu)
admin.site.register(Perustiedot)


