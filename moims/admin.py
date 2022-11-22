from django.contrib import admin
from .models import Moim, CrewJoin, LeaderApply

@admin.register(Moim)
class MoimAdmin(admin.ModelAdmin):

  ''' Moim Admin Definition '''

  list_display = ("title", "owner")
  list_filter = ("moim_types", "topics")


@admin.register(CrewJoin)
class CrewJoinAdmin(admin.ModelAdmin):

  ''' CrewJoin Admin Definition '''
  pass


@admin.register(LeaderApply)
class LeaderApplyAdmin(admin.ModelAdmin):

  ''' LeaderApply Admin Definition '''
  pass
