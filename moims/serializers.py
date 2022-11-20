from rest_framework.serializers import ModelSerializer, SlugRelatedField, SerializerMethodField
from .models import Moim


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

    moim_owner = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    leader = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = Moim
        fields = "__all__"

    def get_current_number_of_participants(self, moim):
        return moim.get_number_of_participants()

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

    moim_owner = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Moim
        fields = (
            "moim_owner",
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
        )

    def get_current_number_of_participants(self, moim):
        return moim.get_number_of_participants()


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
    
    moim_owner = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    
    class Meta:
        model = Moim
        fields = (
            "moim_owner",
            "title",
            "max_participants",
            "min_participants",
            "leader",
            "current_number_of_participants",
            "moim_types",
            "topics",
            "target_amount",
            "expiration_date",
        )

    def get_current_number_of_participants(self, moim):
        return moim.get_number_of_participants()