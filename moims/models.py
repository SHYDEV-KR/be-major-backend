from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from common.models import CommonModel

# Create your models here.
class Moim(CommonModel):

  ''' Moim Model Definition '''

  moim_owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='owning_moims')
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
  has_default_leader = models.BooleanField(default=False)
  leader = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
  participants = models.ManyToManyField('users.User', related_name='participating_moims')
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
  is_full = models.BooleanField(default=False)


class LeaderApply(CommonModel):
  
  ''' LeaderApply Model Definition '''

  moim = models.ForeignKey('Moim', on_delete=models.CASCADE)
  owner = models.ForeignKey('users.User', related_name='moims_applied_as_leader', on_delete=models.CASCADE)
  description = models.TextField(max_length=1000)
  portfolio = models.ManyToManyField('portfolios.Portfolio')
  
  class Meta:
        verbose_name_plural = 'Leader Applies'


class CrewJoin(CommonModel):

  ''' CrewJoin Model Definition '''

  moim = models.ForeignKey('Moim', on_delete=models.CASCADE)
  owner = models.ForeignKey('users.User', related_name='moims_joined_as_crew', on_delete=models.CASCADE)
  description = models.TextField(max_length=1000)
