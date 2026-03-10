from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Team
from .serializers import TeamSerializer


class TeamListCreateView(generics.ListCreateAPIView):

    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TeamDetailView(generics.RetrieveAPIView):

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]