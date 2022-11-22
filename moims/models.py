from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

from django.forms import ValidationError
from common.models import CommonModel

# Create your models here.
class Moim(CommonModel):

  ''' Moim Model Definition '''

  owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='owning_moims')
  title = models.CharField(max_length=200)
  max_participants = models.PositiveIntegerField(
    validators=[
      MinValueValidator(1)
    ],
    default=1
  )
  min_participants = models.PositiveIntegerField(
    validators=[
      MinValueValidator(1)
    ],
    default=1
  )
  description = models.TextField(max_length=2000, null=True, blank=True)
  leader = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
  moim_types = models.ManyToManyField('moim_types.MoimType')
  topics = models.ManyToManyField('topics.Topic')
  is_online = models.BooleanField(default=False)
  location = models.CharField(max_length=100)
  target_amount = models.PositiveIntegerField(
    validators=[
            MaxValueValidator(100000000),
            MinValueValidator(1000)
    ]
  )
  expiration_date = models.DateField(default=datetime.now)
  first_date = models.DateField(default=datetime.now)
  total_moim_times = models.PositiveIntegerField(
    validators=[MinValueValidator(1)]
  )
  is_closed = models.BooleanField(default=False)

  def save(self, *args, **kwargs):
    if self.min_participants > self.max_participants:
      raise ValidationError("min participants more than max participants.")

    if self.expiration_date > self.first_date:
      raise ValidationError("Moim article should expire before first date.")
    
    return super().save(*args, **kwargs)

  def __str__(self):
    return self.title

  def get_number_of_participants(self):
    return self.crewjoin_set.count()


class LeaderApply(CommonModel):
  
  ''' LeaderApply Model Definition '''

  moim = models.ForeignKey('Moim', on_delete=models.CASCADE)
  owner = models.ForeignKey('users.User', related_name='moims_applied_as_leader', on_delete=models.CASCADE)
  description = models.TextField(max_length=1000)
  portfolio = models.ManyToManyField('portfolios.Portfolio')


  def __str__(self):
    return f'[{self.moim}] leader apply : <User {self.owner}>'


  class Meta:
    verbose_name_plural = 'Leader Applies'


class CrewJoin(CommonModel):

  ''' CrewJoin Model Definition '''

  moim = models.ForeignKey('Moim', on_delete=models.CASCADE)
  owner = models.ForeignKey('users.User', related_name='moims_joined_as_crew', on_delete=models.CASCADE)
  description = models.TextField(max_length=1000)

  def __str__(self):
    return f'[{self.moim}] crew join : <User {self.owner}>'

