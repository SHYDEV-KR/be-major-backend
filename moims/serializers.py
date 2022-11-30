from dataclasses import field
from django.http import request
from rest_framework.serializers import ModelSerializer, SlugRelatedField, SerializerMethodField
from rest_framework import serializers
from .models import CrewJoin, LeaderApply, Moim
from portfolios.serializers import UrlMinimalSerializer
from users.serializers import PublicProfileSerializer
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

    current_number_of_participants = SerializerMethodField()
    owner = PublicProfileSerializer()
    leader = PublicProfileSerializer(read_only=True)
    joined_crews = SerializerMethodField()
    applied_leaders = SerializerMethodField()
    is_crew = SerializerMethodField()
    is_leader = SerializerMethodField()
    is_owner = SerializerMethodField()
    has_leader = SerializerMethodField()
    has_applied = SerializerMethodField()


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
        if request.user.is_authenticated and request.user.profile:
            return moim.crewjoin_set.filter(owner=request.user.profile.id).exists()
        return False

    def get_is_leader(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            if moim.leader:
                return moim.leader.id == request.user.profile.id
        return False

    def get_is_owner(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            return moim.owner.id == request.user.profile.id
        return False


    def get_has_leader(self, moim):
        if moim.leader:
            return True
        return False

    def get_has_applied(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            return request.user.profile.leader_applies.filter(moim=moim.id).exists()
        return False


class MoimDetailFromLeaderAppliesSerializer(ModelSerializer):
    moim = MoimDetailSerializer()

    class Meta:
        model = LeaderApply
        fields = ("moim",)

class MoimDetailFromCrewjoinsSerializer(ModelSerializer):
    moim = MoimDetailSerializer()

    class Meta:
        model = CrewJoin
        fields = ("moim",)


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

    leader = PublicProfileSerializer()

    owner = PublicProfileSerializer()

    is_crew = SerializerMethodField()
    is_leader = SerializerMethodField()
    is_owner = SerializerMethodField()
    has_leader = SerializerMethodField()
    has_applied = SerializerMethodField()
    my_leader_apply_id = SerializerMethodField()
    my_crew_join_id = SerializerMethodField()
    leader_apply_id = SerializerMethodField()

    class Meta:
        model = Moim
        fields = (
            "id",
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
            "location",
            "is_crew",
            "is_leader",
            "is_owner",
            "has_leader",
            "has_applied",
            "my_leader_apply_id",
            "my_crew_join_id",
            "leader_apply_id"
        )

    def get_current_number_of_participants(self, moim):
        return moim.get_number_of_participants()

    def get_is_crew(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            return moim.crewjoin_set.filter(owner=request.user.profile.id).exists()
        return False

    def get_is_leader(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            if moim.leader:
                return moim.leader.id == request.user.profile.id
        return False

    def get_is_owner(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            return moim.owner.id == request.user.profile.id
        return False

    def get_has_leader(self, moim):
        if moim.leader:
            return True
        return False

    def get_has_applied(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            return request.user.profile.leader_applies.filter(moim=moim.id).exists()
        return False

    def get_my_leader_apply_id(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            if request.user.profile.leader_applies.filter(moim=moim.id).exists():
                return request.user.profile.leader_applies.get(moim=moim.id).id
        return 0

    def get_my_crew_join_id(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            if request.user.profile.crew_joins.filter(moim=moim.id).exists():
                return request.user.profile.crew_joins.get(moim=moim.id).id
        return 0

    def get_leader_apply_id(self, moim):
        if moim.leader:
            if moim.leader.leader_applies.filter(moim=moim.id).exists():
                return moim.leader.leader_applies.get(moim=moim.id).id
        return 0



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
    leader = PublicProfileSerializer()  
    owner = PublicProfileSerializer()

    is_crew = SerializerMethodField()
    is_leader = SerializerMethodField()
    is_owner = SerializerMethodField()
    has_leader = SerializerMethodField()
    
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
            "has_leader",
        )

    def get_current_number_of_participants(self, moim):
        return moim.get_number_of_participants()

    def get_is_crew(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            return moim.crewjoin_set.filter(owner=request.user.profile.id).exists()
        return False

    def get_is_leader(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            if moim.leader:
                return moim.leader.id == request.user.profile.id
        return False

    def get_has_leader(self, moim):
        if moim.leader:
            return True
        return False

    def get_is_owner(self, moim):
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile:
            return moim.owner.id == request.user.profile.id
        return False


class CrewJoinMinimalSerializer(ModelSerializer):
    owner = PublicProfileSerializer(read_only=True)
    class Meta:
        model = CrewJoin
        fields = ("id", "moim", "description", "owner")

class LeaderApplyMinimalSerializer(ModelSerializer):
    portfolios = UrlMinimalSerializer(
        read_only=True,
        many=True,
    )
    owner = PublicProfileSerializer(read_only=True)

    class Meta:
        model = LeaderApply
        fields = ("id", "moim", "description", "owner", "portfolios")


class CrewJoinSerializer(ModelSerializer):
    owner = PublicProfileSerializer(read_only=True)
    moim = MoimMinimalSerializer(read_only=True)
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