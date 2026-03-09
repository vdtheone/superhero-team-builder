from django.urls import path
from .views import SuperheroListView, SuperheroDetailView

urlpatterns = [
    path("", SuperheroListView.as_view()),
    path("<int:pk>/", SuperheroDetailView.as_view()),
]