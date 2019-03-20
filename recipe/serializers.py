"""Serializers for project_recipe APIs"""


from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import ValidationError

from recipe.fields import IngredientField, RecipeField, StepField, UserField
from recipe.models import Ingredient, Recipe, Step, User


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize a user. 
    """
    url = serializers.HyperlinkedIdentityField(view_name='user-detail',
                                               lookup_field='username',
                                               format='html')
    recipe = RecipeField()
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'recipe')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serialize a recipe. 
    """
    url = serializers.HyperlinkedIdentityField(view_name='recipe-detail',
                                               lookup_field='name',
                                               format='html')
    user = UserField()
    steps = StepField()
    ingredients = IngredientField()
    class Meta:
        model = Recipe
        fields = ('url', 'name', 'user', 'steps', 'ingredients')

    def create(self, validated_data):
        """
        Create a recipe instance.
        """
        username = validated_data['user']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail='User not found.')

        name = validated_data['name']
        try:
            obj = Recipe.objects.get(user=user)
            raise ValidationError('recipe already exists for this user.')
        except Recipe.DoesNotExist:
            recipe = Recipe(name=name, user=user)
            recipe.save()

        steps = validated_data['steps']
        if steps:
            for step in steps:
                obj = Step(name=step, recipe=recipe)
                obj.save()

        ingredients = validated_data['ingredients']
        if ingredients:
            for ingredient in ingredients:
                obj = Ingredient(name=ingredient, recipe=recipe)
                obj.save()

        return recipe

    def update(self, instance, validated_data):
        """
        Update a recipe instance.
        """
        username = validated_data['user']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail='User not found.')
        try:
            recipe = Recipe.objects.get(user=user)
            if recipe != instance:
                raise ValidationError('recipe already exists for this user.')
        except Recipe.DoesNotExist:
            instance.user = user
        
        instance.name = validated_data['name']
        instance.save()

        steps = validated_data['steps']
        step_qs = Step.objects.filter(recipe=instance).values_list('name', flat=True)
        for step in step_qs:
            if step in steps:
                steps.remove(step)
            else:
                Step.objects.filter(recipe=instance, name=step).delete()
        if steps:
            for step in steps:
                obj = Step(name=step, recipe=instance)
                obj.save()

        ingredients = validated_data['ingredients']
        ingredient_qs = Ingredient.objects.filter(recipe=instance).values_list('name', flat=True)
        for ingredient in ingredient_qs:
            if ingredient in ingredients:
                ingredients.remove(ingredient)
            else:
                Ingredient.objects.filter(recipe=instance, name=ingredient).delete()
        if ingredients:
            for ingredient in ingredients:
                obj = Ingredient(name=ingredient, recipe=instance)
                obj.save()
        return instance

