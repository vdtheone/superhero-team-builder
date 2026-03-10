from rest_framework import serializers
from .models import Favourite


class FavouriteSerializer(serializers.ModelSerializer):

    hero_name = serializers.CharField(
        source="superhero.name",
        read_only=True
    )

    class Meta:
        model = Favourite
        fields = [
            "id",
            "superhero",
            "hero_name",
            "created_at",
        ]