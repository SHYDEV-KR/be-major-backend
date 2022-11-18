from django.db import models
from common.models import CommonModel

# Create your models here.
class MoimType(CommonModel):

  ''' MoimType Model Definition '''

  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name