# project_recipe

API:
<br />
<br />
`/users/` - list all the users<br />
`/users/{username}/` - view a user instance and the recipe related to the user<br />
<br />
`/recipes/` - list all the recipes and create a new recipe<br />
`/recipes/{name}/` - update and delete a recipe<br />
<br />
* A new user can be created in the django admin site. Multiple recipes cannot be added to a particular user since the Recipe and User Models have a one to one relationship.
* There is no authentication added to the project.
