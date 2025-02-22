from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('age', 'address', 'last_donation_date', 'is_available', 'blood_group')

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'email')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

# Unregister default User admin and register custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)