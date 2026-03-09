from django.db import models

# Create your models here.
class Superhero(models.Model):

    ALIGNMENT_CHOICES = [
        ("hero", "Hero"),
        ("villain", "Villain"),
        ("neutral", "Neutral"),
    ]

    name = models.CharField(max_length=255)
    alignment = models.CharField(max_length=20, choices=ALIGNMENT_CHOICES)

    intelligence = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)
    durability = models.IntegerField(null=True, blank=True)
    power = models.IntegerField(null=True, blank=True)
    combat = models.IntegerField(null=True, blank=True)

    publisher = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name