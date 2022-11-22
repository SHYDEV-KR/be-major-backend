from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Career, Education, Portfolio, Url

class PortfolioMinimalSerializer(ModelSerializer):
  topics = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
  class Meta:
      model = Portfolio
      fields = ("id", "title", "topics", "bio")


class UrlSerializer(ModelSerializer):
  class Meta:
      model = Url
      fields = "__all__"

class CareerSerializer(ModelSerializer):
  class Meta:
      model = Career
      fields = "__all__"

class EducationSerializer(ModelSerializer):
  class Meta:
      model = Education
      fields = "__all__"


class PortfolioDetailSerializer(ModelSerializer):
  topics = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
  )

  urls = UrlSerializer(many=True, read_only=True)
  careers = CareerSerializer(many=True, read_only=True)
  education = EducationSerializer(many=True, read_only=True)

  class Meta:
    model = Portfolio
    fields = "__all__"


class PortfolioViewSetSerializer(ModelSerializer):
  class Meta:
    model = Portfolio
    fields = "__all__"