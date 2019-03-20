"""Django admin site for project_recipe"""

from django.contrib import admin

from recipe.models import Ingredient, Recipe, Step 

admin.site.register(Recipe)
admin.site.register(Step)
admin.site.register(Ingredient)
