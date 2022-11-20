from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, ParseError
from rest_framework.response import Response
from .models import Moim
from topics.models import Topic
from moim_types.models import MoimType
from users.models import User
from .serializers import MoimDetailSerializer, MoimPublicDetailSerializer, MoimMinimalSerializer
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class MoimList(APIView):

  permission_classes = [IsAuthenticatedOrReadOnly]

  def get(self, request):

    ''' Show Moim List '''

    all_moims = Moim.objects.all()
    serializer = MoimMinimalSerializer(all_moims, many=True)
    return Response(serializer.data)


  def post(self, request):

    ''' Create Moim '''

    def add_topics_to_moim_from_request(request, moim):
      topics = request.data.get("topics")
      for topic_id in topics:
        topic = Topic.objects.get(pk=topic_id)
        moim.topics.add(topic)


    def add_moim_types_to_moim_from_request(request, moim):
      moim_types = request.data.get("moim_types")
      for moim_type_id in moim_types:
        moim_type = MoimType.objects.get(pk=moim_type_id)
        moim.moim_types.add(moim_type)


    def create_moim_with_response(serializer):
      with transaction.atomic(): ## 오류없이 통과하면 코드 한 번에 실행
        new_moim = serializer.save(moim_owner=request.user)
        try:
          add_topics_to_moim_from_request(request, new_moim)
        except Exception:
          raise ParseError("Topic not found.")

        try:
          add_moim_types_to_moim_from_request(request, new_moim)
        except Exception as e:
          raise ParseError("MoimType not found.")

        if request.data.get("leader"):
          try:
            leader_id = request.data.get("leader")
            leader = User.objects.get(pk=leader_id)
            new_moim.leader.add(leader)
          except Exception as e:
            raise ParseError("Leader not found.")


        return Response(
          MoimDetailSerializer(new_moim).data,
        )

    serializer = MoimDetailSerializer(data=request.data)
    if serializer.is_valid():
      return create_moim_with_response(serializer)
    else:
      return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)


class MoimDetail(APIView):
  def get_object(self, id):
    try:
      return Moim.objects.get(pk=id)
    except Moim.DoesNotExist:
      raise NotFound

  def get(self, request, moim_id):
    moim = self.get_object(moim_id)
    serializer = MoimPublicDetailSerializer(moim)
    return Response(serializer.data)


class MoimDetailForOwner(APIView):
  def get_object(self, id):
    try:
      return Moim.objects.get(pk=id)
    except Moim.DoesNotExist:
      raise NotFound

  def get(self, request, moim_id):
    moim = self.get_object(moim_id)
    serializer = MoimSerializer(moim)
    return Response(serializer.data)


  def delete(self, request, moim_id):
    moim = self.get_object(moim_id)
    if not request.user.is_authenticated:
      raise NotAuthenticated
    if moim.owner != request.user:
      raise PermissionDenied