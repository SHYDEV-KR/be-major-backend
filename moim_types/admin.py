from django.contrib import admin
from .models import MoimType

@admin.register(MoimType)
class MoimTypeAdmin(admin.ModelAdmin):

  ''' MoimType Admin Definition '''
  pass
