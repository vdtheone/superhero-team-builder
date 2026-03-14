from rest_framework import generics, filters, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Superhero
from .serializers import SuperheroSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin/staff users to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class SuperheroListView(generics.ListAPIView):
    queryset = Superhero.objects.all().order_by('name')
    serializer_class = SuperheroSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'intelligence', 'strength', 'speed', 'power', 'combat', 'durability']


class SuperheroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Superhero.objects.all()
    serializer_class = SuperheroSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(is_edited=True)

    def get(self, request, *args, **kwargs):
        print("============================", request)
        return super().get(request, *args, **kwargs)