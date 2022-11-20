from django.db import models
from common.models import CommonModel

# Create your models here.
class Portfolio(CommonModel):

  ''' Portfolio Model Definition '''

  owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  topic = models.ManyToManyField('topics.Topic')
  bio = models.TextField(max_length=1000, null=True, blank=True)
  urls = models.ManyToManyField('Url', blank=True)
  careers = models.ManyToManyField('Career', blank=True)
  education = models.ManyToManyField('Education', blank=True)

  def __str__(self) -> str:
    return self.title


class Url(CommonModel):

  ''' Url Model Definition '''

  title = models.CharField(max_length=50)
  short_description = models.CharField(max_length=100, null=True, blank=True)
  url = models.URLField()

  def __str__(self):
    return self.title


class Career(CommonModel):

  ''' Career Model Definition '''

  description = models.CharField(max_length=100)
  start = models.DateField()
  end = models.DateField(null=True, blank=True)
  is_current_job = models.BooleanField(default=False)

  def __str__(self):
    if self.is_current_job:
      return f'[{self.start}~{self.end}] {self.description}'
    else:
      return f'[{self.start}~] {self.description}'


class Education(CommonModel):

  ''' Education Model Definition '''

  description = models.CharField(max_length=100)

  def __str__(self):
    return self.description