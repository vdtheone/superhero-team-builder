from django.db import models
from django.conf import settings
from superheroes.models import Superhero


class Team(models.Model):
    """
    Represents a team of superheroes
    """

    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teams"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    """
    Represents superheroes belonging to a team
    """

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members"
    )

    superhero = models.ForeignKey(
        Superhero,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.superhero.name} in {self.team.name}"