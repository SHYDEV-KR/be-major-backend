from rest_framework.serializers import ModelSerializer, SlugRelatedField, SerializerMethodField
from .models import Career, Education, Portfolio, Url

class UrlSerializer(ModelSerializer):
  is_owner = SerializerMethodField()
  class Meta:
      model = Url
      exclude = ("owner",)

  def get_is_owner(self, url):
    request = self.context.get("request")
    if request:
      return url.owner.id == request.user.profile.id
    return False

class UrlMinimalSerializer(ModelSerializer):
  is_owner = SerializerMethodField()
  class Meta:
      model = Url
      fields = ("id", "title", "short_description", "url", "is_owner")
  
  def get_is_owner(self, url):
    request = self.context.get("request")
    if request:
      return url.owner.id == request.user.profile.id
    return False

class CareerSerializer(ModelSerializer):
  is_owner = SerializerMethodField()
  class Meta:
      model = Career
      exclude = ("owner",)

  def get_is_owner(self, career):
    request = self.context.get("request")
    if request:
      return career.owner.id == request.user.profile.id
    return False

class CareerMinimalSerializer(ModelSerializer):
  name = SerializerMethodField()
  class Meta:
      model = Career
      fields = ("id", "name",)
  
  def get_name(self, career):
    return str(career)

class EducationSerializer(ModelSerializer):
  is_owner = SerializerMethodField()
  class Meta:
      model = Education
      exclude = ("owner",)

  def get_is_owner(self, education):
    request = self.context.get("request")
    if request:
      return education.owner.id == request.user.profile.id
    return False

class EducationMinimalSerializer(ModelSerializer):
  name = SerializerMethodField()
  class Meta:
      model = Education
      fields = ("id", "name",)

  def get_name(self, education):
    return str(education)

class PortfolioDetailSerializer(ModelSerializer):
  topics = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
  )
  is_owner = SerializerMethodField()

  urls = UrlSerializer(many=True, read_only=True)
  careers = CareerSerializer(many=True, read_only=True)
  education = EducationSerializer(many=True, read_only=True)

  class Meta:
    model = Portfolio
    fields = "__all__"

  def get_is_owner(self, portfolio):
    request = self.context.get("request")
    if request:
      return portfolio.owner.id == request.user.profile.id
    return False


class PortfolioViewSetSerializer(ModelSerializer):
  class Meta:
    model = Portfolio
    fields = "__all__"

class PortfolioMinimalSerializer(ModelSerializer):
  topics = SlugRelatedField(
    many=True,
    read_only=True,
    slug_field='name'
  )
  urls = UrlMinimalSerializer(
    many=True,
    read_only=True
  )
  careers = CareerMinimalSerializer(
    many=True,
    read_only=True
  )
  education = EducationMinimalSerializer(
    many=True,
    read_only=True
  )

  class Meta:
    model = Portfolio
    fields = ("id", "title", "topics", "bio", "urls", "careers", "education")
