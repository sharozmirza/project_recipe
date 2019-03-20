"""Fields to be used for the serializers"""

from rest_framework import serializers
from rest_framework.validators import ValidationError

from recipe.models import Ingredient, Step

class UserField(serializers.Field):
    """
    User field
    """
    def to_representation(self, value):
        return value.username

    def to_internal_value(self, data):
        if type(data) != str:
            raise ValidationError('a string is required.')
        return data

class RecipeField(serializers.Field):
    """
    Recipe field
    """
    def to_representation(self, value):
        return value.name

class StepField(serializers.Field):
    """
    Step Field
    """
    def to_representation(self, value):
        val = []
        steps = Step.objects.filter(recipe=value.instance)
        if steps:
            for step in steps:
                val.append(step.name)
        return val

    def to_internal_value(self, data):
        if type(data) != list:
            raise ValidationError('a list of strings is required')
        if data:
            if not all(isinstance(x, str) for x in data):
                raise ValidationError('a list of strings is required')
        return data

class IngredientField(serializers.Field):
    """
    Ingredient Field
    """
    def to_representation(self, value):
        val = []
        ingredients = Ingredient.objects.filter(recipe=value.instance)
        if ingredients:
            for ingredient in ingredients:
                val.append(ingredient.name)
        return val

    def to_internal_value(self, data):
        if type(data) != list:
            raise ValidationError('a list of strings is required')
        if data:
            if not all(isinstance(x, str) for x in data):
                raise ValidationError('a list of strings is required')
        return data
