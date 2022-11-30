from django.db import models
from common.models import CommonModel

# Create your models here.
class MoimTypeManager(models.Manager):
  def create_moim_type(self, name):
    moim_type = self.create(name=name)
    return moim_type

class MoimType(CommonModel):

  ''' MoimType Model Definition '''

  name = models.CharField(max_length=100)
  objects = MoimTypeManager()

  def __str__(self):
    return self.name