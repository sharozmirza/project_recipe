"""Models for project_recipe"""

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


User._meta.get_field('email')._unique = True

class Recipe(models.Model):
    """
    Recipe Model
    """
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
       return self.name

class Step(models.Model):
    """
    Step Model
    """
    name = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')

    def __str__(self):
       return self.name

class Ingredient(models.Model):
    """
    Ingredient Model
    """
    name = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
       return self.name
