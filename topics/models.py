from django.db import models
from common.models import CommonModel

# Create your models here.

class TopicManager(models.Manager):
  def create_topic(self, name):
    topic = self.create(name=name)
    return topic

class Topic(CommonModel):

  ''' Topic Model Definition '''

  name = models.CharField(max_length=100)
  objects = TopicManager()
  
  def __str__(self):
    return self.name