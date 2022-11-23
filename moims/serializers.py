from dataclasses import field
from rest_framework.serializers import ModelSerializer, SlugRelatedField, SerializerMethodField
from rest_framework import serializers
from .models import CrewJoin, LeaderApply, Moim
from portfolios.serializers import PortfolioMinimalSerializer
from rest_framework.exceptions import ValidationError
import datetime



class MoimDetailSerializer(ModelSerializer):
    topics = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    moim_types = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    participants = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )

    current_number_of_participants = SerializerMethodField()

    owner = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    leader = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )


    joined_crews = SerializerMethodField()
    applied_leaders = SerializerMethodField()

    is_crew = SerializerMethodField()
    is_leader = SerializerMethodField()
    is_owner = SerializerMethodField()


    class Meta:
        model = Moim
        fields = "__all__"

    def validate_expiration_date(self, expiration_date):
        now = datetime.date.today()
        if now > expiration_date:
            raise serializers.ValidationError("expiration date invalid.")
        return expiration_date
    
    def validate_first_date(self, first_date):
        now = datetime.date.today()
        if now > first_date:
            raise serializers.ValidationError("first date invalid.")
        return first_date

    def validate(self, data):
        if data['min_participants'] > data['max_participants']:
            raise serializers.ValidationError("min participants more than max participants.")

        if data['expiration_date'] >= data['first_date']:
            raise serializers.ValidationError("expiration date should be earlier than first date.")
        
        return data

    def get_current_number_of_participants(self, moim):
        return moim.get_number_of_participants()

    def get_joined_crews(self, moim):
        return CrewJoinMinimalSerializer(moim.crewjoin_set.all(), many=True, read_only=True).data

    def get_applied_leaders(self, moim):
        return LeaderApplyMinimalSerializer(moim.leaderapply_set.all(), many=True, read_only=True).data
    
    def get_is_crew(self, moim):
        request = self.context.get("request")
        if request:
            print(moim.crewjoin_set.all())
            return moim.crewjoin_set.filter(owner=request.user).exists()
        return False

    def get_is_leader(self, moim):
        request = self.context.get("request")
        if request:
            return moim.leader == request.user
        return False

    def get_is_owner(self, moim):
        request = self.context.get("request")
        if request:
            return moim.owner == request.user
        return False


class MoimPublicDetailSerializer(ModelSerializer):
    topics = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    moim_types = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    current_number_of_participants = SerializerMethodField()

    leader = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    owner = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    is_crew = SerializerMethodField()
    is_leader = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model = Moim
        fields = (
            "owner",
            "title",
            "max_participants",
            "min_participants",
            "current_number_of_participants",
            "leader",
            "moim_types",
            "topics",
            "target_amount",
            "expiration_date",
            "description",
            "first_date",
            "total_moim_times",
            "is_crew",
            "is_leader",
            "is_owner",
        )

    def get_current_number_of_participants(self, moim):
        return moim.get_number_of_participants()

    def get_is_crew(self, moim):
        request = self.context.get("request")
        if request:
            return moim.crewjoin_set.filter(owner=request.user).exists()
        return False

    def get_is_leader(self, moim):
        request = self.context.get("request")
        if request:
            return moim.leader == request.user
        return False

    def get_is_owner(self, moim):
        request = self.context.get("request")
        if request:
            return moim.owner == request.user
        return False



class MoimMinimalSerializer(ModelSerializer):
    topics = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    moim_types = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    current_number_of_participants = SerializerMethodField()
    leader = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    
    owner = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    is_crew = SerializerMethodField()
    is_leader = SerializerMethodField()
    is_owner = SerializerMethodField()
    
    class Meta:
        model = Moim
        fields = (
            "id",
            "owner",
            "title",
            "max_participants",
            "min_participants",
            "leader",
            "current_number_of_participants",
            "moim_types",
            "topics",
            "target_amount",
            "expiration_date",
            "is_crew",
            "is_leader",
            "is_owner",
        )

    def get_current_number_of_participants(self, moim):
        return moim.get_number_of_participants()

    def get_is_crew(self, moim):
        request = self.context.get("request")
        if request:
            return moim.crewjoin_set.filter(owner=request.user).exists()
        return False

    def get_is_leader(self, moim):
        request = self.context.get("request")
        if request:
            return moim.leader == request.user
        return False

    def get_is_owner(self, moim):
        request = self.context.get("request")
        if request:
            return moim.owner == request.user
        return False


class CrewJoinMinimalSerializer(ModelSerializer):
    class Meta:
        model = CrewJoin
        fields = ("description", "owner")

class LeaderApplyMinimalSerializer(ModelSerializer):
    portfolios = PortfolioMinimalSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = LeaderApply
        fields = ("description", "owner", "portfolios")


class CrewJoinSerializer(ModelSerializer):
    class Meta:
        model = CrewJoin
        fields = "__all__"

class LeaderApplySerializer(ModelSerializer):
    class Meta:
        model = LeaderApply
        fields = "__all__"


class CrewJoinListSerializer(ModelSerializer):
    moim = MoimMinimalSerializer()
    class Meta:
        model = CrewJoin
        fields = "__all__"


class LeaderApplyListSerializer(ModelSerializer):
    moim = MoimMinimalSerializer()
    class Meta:
        model = LeaderApply
        fields = "__all__"