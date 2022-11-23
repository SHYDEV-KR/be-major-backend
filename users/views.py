from django.contrib.auth import login, logout, authenticate
from django.db import transaction
from django.db.models import Q, Prefetch

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound, AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.views import APIView

from random import randint
from moims.models import CrewJoin, Moim

from .models import SMSAuth, User, Profile
from . import serializers
from portfolios import serializers as portfolios_serializers
from moims import serializers as moims_serializers

# Create your views here.
class UserCreate(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = serializers.UserSerializer

  def create(self, request, *args, **kwargs):
    try:
      sms_auth = SMSAuth.objects.get(phone_number=request.data.get('phone_number'))
      if not sms_auth.is_phone_number_authenticated:
        raise AuthenticationFailed
    except:
      return Response({"message": "phone number is unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    return super().create(request, *args, **kwargs)


class MyAccount(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):

    ''' Show Logged in User's Account '''

    user = request.user
    serializer = serializers.PrivateUserSerializer(user)
    return Response(serializer.data)

  def put(self, request):
  
    ''' Edit User's Account '''
  
    user = request.user
    serializer = serializers.PrivateUserSerializer(
        user,
        data=request.data,
        partial=True,
    )
    if serializer.is_valid():
        user = serializer.save()
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


class MyProfile(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):

    ''' Show Logged in User's Profile '''
    try:
      user = request.user
      user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
      raise NotFound
    serializer = serializers.PrivateProfileSerializer(user_profile)
    return Response(serializer.data)


  def put(self, request):
  
    ''' Edit User's Profile '''
  
    try:
      user = request.user
      user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
      raise NotFound
    serializer = serializers.PrivateProfileSerializer(
      user_profile, 
      data=request.data, 
      partial=True,
    )
    
    if serializer.is_valid():
      user_profile = serializer.save()
      serializer = serializers.PrivateProfileSerializer(user_profile)
      return Response(serializer.data)
    else:
      return Response(serializer.errors)


class ChangePassword(APIView):

  permission_classes = [IsAuthenticated]

  def put(self, request):

    ''' Receive old_password, new_password '''

    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    if not old_password or not new_password:
        raise ParseError
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)
    else:
      raise ParseError("password is wrong.")


class LogIn(APIView):
  def post(self, request):
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")
    if not phone_number or not password:
      raise ParseError
    user = authenticate(
      request,
      phone_number=phone_number,
      password=password
    )
    if user:
      login(request, user)
      return Response(serializers.PrivateUserSerializer(user).data)
    else:
      return Response({"error": "wrong password"})


class LogOut(APIView):
  
  permission_classes = [IsAuthenticated]

  def post(self, request):
    logout(request)
    return Response({"ok": "bye!"})


class PublicUserProfile(APIView):
  def get(self, request, username):
    try:
      user = User.objects.get(username=username)
      user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
      raise NotFound
    serializer = serializers.PublicProfileSerializer(user_profile)
    return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = serializers.PrivateProfileSerializer

  permission_classes = [IsAuthenticated]

  def create(self, request):
    user = request.user
    if Profile.objects.filter(user=user).exists():
      raise ParseError("user already has profile")
    
    with transaction.atomic():  
      serializer = self.get_serializer(data=request.data)
      if serializer.is_valid():
        new_profile = serializer.save(user=user)
        return Response(serializers.PrivateProfileSerializer(new_profile).data)
      else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class SMSAuthView(APIView):
  def post(self, request):

    ''' Send SMS : Receive phone_number'''
    
    try:
      phone_number = request.data['phone_number']
    except KeyError:
      return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    else:
      auth_number = randint(1000, 10000)
      sms_auth, _ = SMSAuth.objects.update_or_create(phone_number=phone_number)
      sms_auth.auth_number = auth_number
      sms_auth.save()
      sms_auth.send_sms()
      return Response({'message': 'OK'})

  def get(self, request):
    try:
      phone_number = request.query_params['phone_number']
      auth_number = request.query_params['auth_number']
    except KeyError:
      return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    
    result = SMSAuth.check_auth_number(phone_number, auth_number)
    if result:
      sms_auth = SMSAuth.objects.get(phone_number=phone_number)
      sms_auth.is_phone_number_authenticated = True
      sms_auth.save()
      return Response({"message": "phone number authenticated"}, status=status.HTTP_200_OK)
    else:
      return Response({"message": "phone number authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)


class UserPortfolio(APIView):
  def get(self, request, username):
    try:
      user = User.objects.get(username=username)
    except:
      raise ParseError
    
    portfolios = user.portfolio_set.all()
    serializer = portfolios_serializers.PortfolioMinimalSerializer(portfolios, many=True, read_only=True)
    return Response(serializer.data)

class UserCareers(APIView):
  def get(self, request, username):
    try:
      user = User.objects.get(username=username)
    except:
      raise ParseError
    
    careers = user.career_set.all()
    serializer = portfolios_serializers.CareerMinimalSerializer(careers, many=True, read_only=True)
    return Response(serializer.data)


class UserUrls(APIView):
  def get(self, request, username):
    try:
      user = User.objects.get(username=username)
    except:
      raise ParseError
    
    urls = user.url_set.all()
    serializer = portfolios_serializers.UrlMinimalSerializer(urls, many=True, read_only=True)
    return Response(serializer.data)


class UserEducation(APIView):
  def get(self, request, username):
    try:
      user = User.objects.get(username=username)
    except:
      raise ParseError
    
    education = user.education_set.all()
    serializer = portfolios_serializers.EducationMinimalSerializer(education, many=True, read_only=True)
    return Response(serializer.data)


class UserMoimAsCrew(APIView):
  def get(self, request, username):
    try:
      user = User.objects.get(username=username)
    except:
      raise ParseError
    
    crew_joins = user.crew_joins.all()
    
    if not crew_joins:
      return Response(status=status.HTTP_204_NO_CONTENT)
    
    serializer = moims_serializers.CrewJoinListSerializer(crew_joins, many=True, read_only=True)
    return Response(serializer.data)


class UserMoimAsLeader(APIView):
  def get(self, request, username):
    try:
      user = User.objects.get(username=username)
    except:
      raise ParseError
    
    leader_applies = user.leader_applies.all()

    if not leader_applies:
      return Response(status=status.HTTP_204_NO_CONTENT)
    
    serializer = moims_serializers.LeaderApplyListSerializer(leader_applies, many=True, read_only=True)
    return Response(serializer.data)


class MyMoims(APIView):
  def get(self, request):
  
    ''' Show Logged in User's Moims '''

    try:
      user = request.user
      owning_moims = Moim.objects.filter(owner=user)
      leader_moims = Moim.objects.filter(leader=user)
      crew_moims = Moim.objects.all().prefetch_related(Prefetch('crewjoin_set', queryset=CrewJoin.objects.filter(owner=user)))
      moims = owning_moims | leader_moims | crew_moims
    except Moim.DoesNotExist:
      raise NotFound
    serializer = moims_serializers.MoimMinimalSerializer(
      moims, 
      many=True, 
      read_only=True, 
      context={'request':request},
    )
    return Response(serializer.data)