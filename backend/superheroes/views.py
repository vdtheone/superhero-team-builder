from rest_framework import generics
from .models import Superhero
from .serializers import SuperheroSerializer


class SuperheroListView(generics.ListAPIView):
    queryset = Superhero.objects.all()
    serializer_class = SuperheroSerializer


class SuperheroDetailView(generics.RetrieveAPIView):
    queryset = Superhero.objects.all()
    serializer_class = SuperheroSerializer