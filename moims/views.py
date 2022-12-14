from datetime import datetime
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, ParseError, ValidationError
from rest_framework.response import Response
from .models import Moim
from . import models
from topics.models import Topic
from portfolios.models import Portfolio
from moim_types.models import MoimType
from users.models import User
from .serializers import CrewJoinMinimalSerializer, CrewJoinSerializer, LeaderApplyMinimalSerializer, MoimDetailSerializer, MoimPublicDetailSerializer, MoimMinimalSerializer, LeaderApplySerializer
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE, HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class MoimList(APIView):

  permission_classes = [IsAuthenticatedOrReadOnly]

  def get(self, request):

    ''' Show Moim List '''

    all_moims = Moim.objects.filter(expiration_date__gte=datetime.now().strftime('%Y-%m-%d')).order_by("-created_at")
    serializer = MoimMinimalSerializer(
      all_moims, 
      many=True, 
      read_only=True, 
      context={"request" : request}
    )
    return Response(serializer.data)


  def post(self, request):

    ''' Create Moim '''

    def add_topics_to_moim_from_request(request, moim):
      topics = request.data.get("topics")
      for topic_name in topics:
        topic = Topic.objects.get(name=topic_name)
        moim.topics.add(topic)


    def add_moim_types_to_moim_from_request(request, moim):
      moim_types = request.data.get("moim_types")
      for moim_type_name in moim_types:
        moim_type = MoimType.objects.get(name=moim_type_name)
        moim.moim_types.add(moim_type)


    def create_moim_with_response(serializer):
      with transaction.atomic(): ## 오류없이 통과하면 코드 한 번에 실행
        new_moim = serializer.save(owner=request.user.profile)
        try:
          add_topics_to_moim_from_request(request, new_moim)
        except Exception:
          raise ParseError("Topic not found.")

        try:
          add_moim_types_to_moim_from_request(request, new_moim)
        except Exception as e:
          raise ParseError("MoimType not found.")

        return Response(
          MoimDetailSerializer(new_moim, context={"request": request}).data,
        )

    print(request.data)

    serializer = MoimDetailSerializer(data=request.data)
    if serializer.is_valid():
      return create_moim_with_response(serializer)
    else:
      print(serializer.errors)
      return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)


class MoimDetail(APIView):
  def get_object(self, id):
    try:
      return Moim.objects.get(pk=id)
    except Moim.DoesNotExist:
      raise NotFound

  def get(self, request, moim_id):
    
    ''' Show Public Moim Detail '''

    moim = self.get_object(moim_id)
    serializer = MoimPublicDetailSerializer(moim, context={'request':request})
    return Response(serializer.data)


class MoimDetailForOwner(APIView):
  permission_classes = [IsAuthenticated]

  def get_object(self, id):
    try:
      return Moim.objects.get(pk=id)
    except Moim.DoesNotExist:
      raise NotFound

  def get(self, request, moim_id):

    ''' Show Private Moim Detail '''

    moim = self.get_object(moim_id)
    
    if moim.owner.id != request.user.profile.id:
      raise PermissionDenied
    
    serializer = MoimDetailSerializer(moim, context={'request':request})
    return Response(serializer.data)


  def delete(self, request, moim_id):
    moim = self.get_object(moim_id)
    if moim.owner.id != request.user.profile.id:
      raise PermissionDenied

    moim.delete()
    return Response(status=HTTP_204_NO_CONTENT)


class ChangeMoimCloseState(APIView):
  permission_classes = [IsAuthenticated]

  def get_object(self, id):
    try:
      return Moim.objects.get(pk=id)
    except Moim.DoesNotExist:
      raise NotFound

  def get(self, request, moim_id):

    ''' Change Moim Close State '''

    moim = self.get_object(moim_id)
    
    if moim.owner != request.user:
      raise PermissionDenied

    if moim.is_closed:
      moim.is_closed = False
    else:
      if moim.get_number_of_participants() < moim.min_participants:
        raise ValidationError("Cannot close moim : not enough number of participants.")
      moim.is_closed = True

    moim.save()

    serializer = MoimDetailSerializer(moim)
    return Response(serializer.data)


class ChooseLeader(APIView):
  permission_classes = [IsAuthenticated]

  def get_object(self, id):
    try:
      return Moim.objects.get(pk=id)
    except Moim.DoesNotExist:
      raise NotFound

  def post(self, request, moim_id):

    ''' Choose Leader of Moim '''

    moim = self.get_object(moim_id)
    
    if moim.owner != request.user:
      raise PermissionDenied
    
    if not request.data.get("leader"):
      raise ParseError

    try:
      leader_id = request.data.get("leader")
      leader = User.objects.get(pk=leader_id)
      if leader == request.user:
        raise ValidationError
    except ValidationError:
      raise ParseError("Cannot be leader")
    except Exception as e:
      raise ParseError("Leader not found.")

    if not moim.leaderapply_set.filter(owner=leader).exists():
      raise ParseError("Leader didn't apply.")
      
    moim.leader = leader
    moim.save()

    serializer = MoimDetailSerializer(moim)
    return Response(serializer.data)



class CrewJoin(APIView):
  permission_classes = [IsAuthenticatedOrReadOnly]

  def get_moim_object(self, id):
    try:
      return Moim.objects.get(pk=id)
    except Moim.DoesNotExist:
      raise NotFound

  def get_crew_join_object(self, id):
    try:
      return models.CrewJoin.objects.get(pk=id)
    except models.CrewJoin.DoesNotExist:
      raise NotFound

  def get(self, request, crew_join_id):
      
    ''' Show Crew Join Detail '''

    crew_join = self.get_crew_join_object(crew_join_id)
    serializer = CrewJoinMinimalSerializer(crew_join, context={'request':request})
    return Response(serializer.data)

  def post(self, request, moim_id):

    ''' Crew : Join Moim '''

    moim = self.get_moim_object(moim_id)
    if moim.crewjoin_set.filter(owner=request.user.profile).exists():
      raise ParseError("Already Joined this moim.")
    if moim.is_closed:
      raise ParseError("Moim closed.")
    if moim.leaderapply_set.filter(owner=request.user.profile).exists():
      raise ParseError("Already Applied to this moim as leader.")
    if moim.crewjoin_set.count() >= moim.max_participants:
      raise ParseError("No more joins available.")

    serializer = CrewJoinSerializer(data=request.data, context={'request':request})
    if serializer.is_valid():
      new_crew_join = serializer.save(owner=request.user.profile, moim=moim)
      return Response(
          CrewJoinSerializer(new_crew_join, context={'request':request}).data,
        )
    else:
      print(serializer.errors)
      return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)


class LeaderApply(APIView):
  permission_classes = [IsAuthenticatedOrReadOnly]

  def get_object(self, id):
    try:
      return Moim.objects.get(pk=id)
    except Moim.DoesNotExist:
      raise NotFound

  def get_leader_apply_object(self, id):
    print(LeaderApply)
    try:
      return models.LeaderApply.objects.get(pk=id)
    except models.LeaderApply.DoesNotExist:
      raise NotFound

  def get(self, request, leader_apply_id):
      
    ''' Show Crew Join Detail '''

    leader_apply = self.get_leader_apply_object(leader_apply_id)
    serializer = LeaderApplyMinimalSerializer(leader_apply, context={'request':request})
    return Response(serializer.data)

  def post(self, request, moim_id):

    ''' Leader : Apply to Moim '''

    moim = self.get_object(moim_id)
    
    if moim.leaderapply_set.filter(owner=request.user).exists():
      raise ParseError("Already Applied to this moim.")
    if moim.crewjoin_set.filter(owner=request.user).exists():
      raise ParseError("Already Joined this moim as crew.")
    if moim.is_closed:
      raise ParseError("Moim closed.")

    serializer = LeaderApplySerializer(data=request.data)
    if serializer.is_valid():
      with transaction.atomic():
        new_leader_apply = serializer.save(owner=request.user, moim=moim)
        try:
          portfolios = request.data.get("portfolios")
          for portfolio_id in portfolios:
            portfolio = Portfolio.objects.get(pk=portfolio_id)
            if portfolio.owner != request.user:
              raise ValidationError
            new_leader_apply.portfolio.add(portfolio)
        except ValidationError:
          raise ParseError("Not owner of portfolio.")
        except Exception as e:
          raise ParseError("Portfolio not found.")


        return Response(
            LeaderApplySerializer(new_leader_apply).data,
          )
    else:
      return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)