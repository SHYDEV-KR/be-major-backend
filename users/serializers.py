from rest_framework import serializers
from .models import User

class MinimalUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields= (
      "avatar",
      "username"
    )