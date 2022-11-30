from asyncore import read
from dataclasses import field
from xml.etree.ElementInclude import include
from django.forms import models
from rest_framework import serializers
from .models import Profile, User


class UserSerializer(serializers.ModelSerializer):
  def create(self, validated_data):
    user = User.objects.create_user(
      phone_number=validated_data['phone_number'],
      username=validated_data['username'],
      password=validated_data['password'],
    )
    return user

  class Meta:
    model = User
    fields= ("phone_number", "username", "password")


class PrivateUserSerializer(serializers.ModelSerializer):

  has_profile = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields= ("phone_number", "username", "has_profile")

  def get_has_profile(self, user):
    try:
      if user.profile:
        return True
    except:
      return False


class PrivateProfileSerializer(serializers.ModelSerializer):
  user = PrivateUserSerializer(read_only=True)

  class Meta:
    model = Profile
    fields= "__all__"


class PublicProfileSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
    read_only=True,
    slug_field='username'
  )

  class Meta:
    model = Profile
    fields = ("id", "user", "avatar",)