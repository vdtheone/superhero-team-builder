from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Team, TeamMember
from .serializers import TeamSerializer, CompareStoredTeamsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.cache import cache
from django.conf import settings
from .serializers import CompareRequestSerializer



class TeamListCreateView(generics.ListCreateAPIView):

    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TeamDetailView(generics.RetrieveUpdateAPIView):

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_update(self, serializer):
        team = serializer.save()
        if 'member_ids' in self.request.data:
            team.members.all().delete()
            for hero_id in self.request.data['member_ids']:
                TeamMember.objects.create(team=team, superhero_id=hero_id)

class TeamDeleteView(generics.DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


from .engine import (
    recommend_balanced,
    recommend_by_stat,
    recommend_random,
    compare_teams,
    _to_dict,
    STAT_FIELDS,
)


class RecommendTeamView(APIView):
    """
    GET /api/teams/recommend/?strategy=balanced&size=6
    GET /api/teams/recommend/?strategy=power&stat=strength&size=6
    GET /api/teams/recommend/?strategy=random&size=6
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        strategy = request.query_params.get("strategy", "balanced")
        size = min(int(request.query_params.get("size", 6)), 12)
        stat = request.query_params.get("stat", "strength")
        refresh = request.query_params.get("refresh", "false").lower() == "true"

        # Cache key for non-random strategies
        cache_key = f"team_recommend_{strategy}_{stat}_{size}"

        if strategy != "random" and not refresh:
            cached = cache.get(cache_key)
            if cached:
                return Response(cached)

        if strategy == "balanced":
            result = recommend_balanced(size)
        elif strategy == "power":
            if stat not in STAT_FIELDS:
                return Response(
                    {"detail": f"Invalid stat. Choose from: {STAT_FIELDS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            result = recommend_by_stat(stat, size)
        elif strategy == "random":
            result = recommend_random(size)
        else:
            return Response(
                {"detail": "Invalid strategy. Choose: balanced | power | random"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if strategy != "random":
            cache.set(cache_key, result, settings.CACHE_TTL_TEAMS)

        return Response(result)


class CompareTeamsView(APIView):
    """
    POST /api/teams/compare/
    Body: { "teams": [{ "name": "...", "members": [...] }, ...] }
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CompareRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        teams_data = serializer.validated_data["teams"]
        result = compare_teams(teams_data)
        return Response(result)


class CompareStoredTeamsView(APIView):
    """
    POST /api/teams/compare_stored/
    Body: { "team_ids": [1, 2] }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CompareStoredTeamsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        team_ids = serializer.validated_data["team_ids"]
        teams = Team.objects.filter(id__in=team_ids, created_by=request.user)

        if teams.count() < 2:
            return Response({"detail": "At least two valid teams are required."}, status=status.HTTP_400_BAD_REQUEST)

        teams_data = []
        for team in teams:
            members = [_to_dict(tm.superhero) for tm in team.members.all()]
            teams_data.append({"name": team.name, "members": members})

        result = compare_teams(teams_data)
        return Response(result)