from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Portfolio

class PortfolioMinimalSerializer(ModelSerializer):
  topic = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
  class Meta:
      model = Portfolio
      fields = ("id", "title", "topic", "bio")

