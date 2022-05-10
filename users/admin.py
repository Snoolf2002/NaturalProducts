from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import MyUser


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)  

    class Meta:
        model  = MyUser
        fields = ('email', 'username', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model               = MyUser
        fields              = ('email', 'password', 'username', 'profile_image', 'is_active', 'is_admin')
        read_only_fields    = ('email',)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form        = UserChangeForm
    add_form    = UserCreationForm

    list_display    = ('email', 'username', 'is_admin')
    list_filter     = ('is_admin',)
    fieldsets       = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password'),
        }),
    )
    search_fields       = ('email', 'username')
    ordering            = ('email',)
    filter_horizontal   = ()


admin.site.register(MyUser, UserAdmin)

admin.site.unregister(Group)