from django.contrib import admin
from .models import Portfolio, Url, Career, Education

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):

  ''' Portfolio Admin Definition '''
  pass

@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):

  ''' Url Admin Definition '''
  pass


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):

  ''' Career Admin Definition '''
  pass


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):

  ''' Education Admin Definition '''
  pass
