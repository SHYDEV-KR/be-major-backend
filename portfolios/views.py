from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework import viewsets

from topics.models import Topic
from .models import Url, Career, Education, Portfolio

# Create your views here.
class PortfolioViewSet(viewsets.ModelViewSet):
  queryset = Portfolio.objects.all()

  permission_classes = [
    IsAuthenticatedOrReadOnly,
  ]

  def get_serializer_class(self):
    if self.action == 'create' or self.action == 'retrieve':
      return serializers.PortfolioDetailSerializer
    return serializers.PortfolioViewSetSerializer


  def create(self, request):
    request.data['owner'] = request.user.id
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      new_portfolio = serializer.save(owner=self.request.user)

      topics = request.data.get("topics")
      for topic_id in topics:
        if not Topic.objects.filter(pk=topic_id).exists():
          raise ParseError("no matching topic.")
        topic = Topic.objects.get(pk=topic_id)
        new_portfolio.topics.add(topic)
      
      urls = request.data.get('urls')
      if urls:
        for url_id in urls:
          if not Url.objects.filter(pk=url_id).exists():
            raise ParseError("no matching url.")
          if not request.user.url_set.filter(pk=url_id).exists():
            raise ParseError("not user url.")
          
          new_portfolio.urls.add(url_id)
        
      
      careers = request.data.get('careers')
      if careers:
        for career_id in careers:
          if not Career.objects.filter(pk=career_id).exists():
            raise ParseError("no matching career.")
          if not request.user.career_set.filter(pk=career_id).exists():
            raise ParseError("not user career")

          new_portfolio.careers.add(career_id)
    
      education = request.data.get('education')
      if education:
        for education_id in education:
          if not Education.objects.filter(pk=education_id).exists():
            raise ParseError("no matching education.")
          if not request.user.education_set.filter(pk=education_id).exists():
            raise ParseError("not user education.")

          new_portfolio.education.add(education_id)

      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)


  def partial_update(self, request, pk=None):
    portfolio = Portfolio.objects.get(pk=pk)
    
    if request.user != portfolio.owner:
      return Response({"detail" : "method only allowed to owner."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    request.data['owner'] = request.user.id

    urls = request.data.get('urls')
    if urls:
      for url_id in urls:
        if not Url.objects.filter(pk=url_id).exists():
          raise ParseError("no url.")
        if not request.user.url_set.filter(pk=url_id).exists():
          raise ParseError("not user url")
      
    careers = request.data.get('careers')
    if careers:
      for career_id in careers:
        if not Career.objects.filter(pk=career_id).exists():
          raise ParseError("no career.")
        if not request.user.career_set.filter(pk=career_id).exists():
          raise ParseError("not user career")
    
    education = request.data.get('education')
    if education:
      for education_id in education:
        if not Education.objects.filter(pk=education_id).exists():
          raise ParseError("no education.")
        if not request.user.education_set.filter(pk=education_id).exists():
          raise ParseError("not user education.")
    

    return super().partial_update(request, pk)


  def destroy(self, request, pk=None):
    portfolio = Portfolio.objects.get(pk=pk)
    
    if request.user != portfolio.owner:
      return Response({"detail" : "method only allowed to owner."}, status=status.HTTP_406_NOT_ACCEPTABLE)

    return super().destroy(request, pk)


class CareerViewSet(viewsets.ModelViewSet):
  queryset = Career.objects.all()
  serializer_class = serializers.CareerSerializer

  permission_classes = [
    IsAuthenticatedOrReadOnly,
  ]

  def partial_update(self, request, pk=None):
    career = Career.objects.get(pk=pk)
    
    if request.user != career.owner:
      return Response({"detail" : "method only allowed to owner."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    return super().partial_update(request, pk)


  def destroy(self, request, pk=None):
    career = Career.objects.get(pk=pk)
    
    if request.user != career.owner:
      return Response({"detail" : "method only allowed to owner."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    return super().destroy(request, pk)


class UrlViewSet(viewsets.ModelViewSet):
  queryset = Url.objects.all()
  serializer_class = serializers.UrlSerializer

  permission_classes = [
    IsAuthenticatedOrReadOnly,
  ]

  def partial_update(self, request, pk=None):
    url = Url.objects.get(pk=pk)
    
    if request.user != url.owner:
      return Response({"detail" : "method only allowed to owner."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    return super().partial_update(request, pk)


  def destroy(self, request, pk=None):
    url = Url.objects.get(pk=pk)
    
    if request.user != url.owner:
      return Response({"detail" : "method only allowed to owner."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    return super().destroy(request, pk)


class EducationViewSet(viewsets.ModelViewSet):
  queryset = Education.objects.all()
  serializer_class = serializers.EducationSerializer

  permission_classes = [
    IsAuthenticatedOrReadOnly,
  ]

  def partial_update(self, request, pk=None):
    education = Education.objects.get(pk=pk)
    
    if request.user != education.owner:
      return Response({"detail" : "method only allowed to owner."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    return super().partial_update(request, pk)


  def destroy(self, request, pk=None):
    education = Education.objects.get(pk=pk)
    
    if request.user != education.owner:
      return Response({"detail" : "method only allowed to owner."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    return super().destroy(request, pk)