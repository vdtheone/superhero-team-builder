from rest_framework import serializers
from .models import Team, TeamMember
from superheroes.models import Superhero


class TeamMemberSerializer(serializers.ModelSerializer):

    superhero_name = serializers.CharField(
        source="superhero.name",
        read_only=True
    )

    class Meta:
        model = TeamMember
        fields = ["id", "superhero", "superhero_name"]


class TeamSerializer(serializers.ModelSerializer):

    members = TeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "created_by",
            "created_at",
            "members",
        ]
        read_only_fields = ["created_by"]