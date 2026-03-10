from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import Favourite
from .serializers import FavouriteSerializer


class FavouriteListView(generics.ListAPIView):

    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)


class FavouriteCreateView(generics.CreateAPIView):

    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        superhero = serializer.validated_data["superhero"]

        if Favourite.objects.filter(
            user=self.request.user,
            superhero=superhero
        ).exists():
            raise ValidationError("Hero already in favourites")

        serializer.save(user=self.request.user)


class FavouriteDeleteView(generics.DestroyAPIView):

    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)