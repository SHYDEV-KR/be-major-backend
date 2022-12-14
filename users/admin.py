from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, SMSAuth


@admin.register(User)
class CustomUserAdmin(UserAdmin):

  ''' User Admin Definition '''

  readonly_fields = ["date_joined"]


  fieldsets = (
    (
      "User Information",
      {
        "fields": ("username",  "phone_number", "password"),
        "classes": ("wide",),
      },
    ),
    (
      "Permissions",
      {
        "fields": (
          "is_active",
          "is_admin",
          "is_superuser",
          "groups",
          "user_permissions",
        ),
        "classes": ("collapse",),
      },
    ),
    (
      "Important Dates",
      {
        "fields": ("last_login", "date_joined"),
        "classes": ("collapse",),
      },
    ),
  )
  add_fieldsets = ((None, {
    'fields': ('username', 'phone_number', 'password1', 'password2')
  }),)

  list_display = ("username", "phone_number")
  list_filter = ('is_admin',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

  ''' Profile Admin Definition '''

  fieldsets = (
    (
      "Profile",
      {
        "fields": ("user", "avatar","major", "email", "gender", "date_of_birth"),
        "classes": ("wide",),
      },
    ),
  )
  list_display = ("user", "email")

@admin.register(SMSAuth)
class SMSAuthAdmin(admin.ModelAdmin):
  pass