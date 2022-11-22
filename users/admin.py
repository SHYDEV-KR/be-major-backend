from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):

  ''' User Admin Definition '''

  fieldsets = (
    (
      "User Information",
      {
        "fields": ("username",  "phone_number", "is_phone_number_authenticated", "password"),
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

  list_display = ("username", "phone_number")
  list_filter = ('is_admin',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

  ''' Profile Admin Definition '''

  fieldsets = (
    (
      "Profile",
      {
        "fields": ("user", "email", "gender", "date_of_birth" ,"is_leader"),
        "classes": ("wide",),
      },
    ),
  )
  list_display = ("user", "is_leader")