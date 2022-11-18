from django.db import models
from common.models import CommonModel

# Create your models here.
class Portfolio(CommonModel):

  ''' Portfolio Model Definition '''

  owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  topic = models.ManyToManyField('topics.Topic')
  bio = models.TextField(max_length=1000)
  urls = models.ManyToManyField('Url')
  careers = models.ManyToManyField('Career')
  education = models.ManyToManyField('Education')


class Url(CommonModel):

  ''' Url Model Definition '''

  title = models.CharField(max_length=50)
  short_description = models.CharField(max_length=100)
  url = models.URLField()

  def __str__(self):
    return self.title


class Career(CommonModel):

  ''' Career Model Definition '''

  description = models.CharField(max_length=100)
  start = models.DateField()
  end = models.DateField()

  def __str__(self):
    return f'[{self.start}~{self.end}] {self.description}'


class Education(CommonModel):

  ''' Education Model Definition '''

  description = models.CharField(max_length=100)

  def __str__(self):
    return self.description