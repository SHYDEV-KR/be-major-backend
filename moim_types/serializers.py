from rest_framework import serializers
from .models import MoimType

class MoimTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = MoimType
    fields = ("name")