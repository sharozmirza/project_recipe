"""Views/APIs for the recipe app."""

from rest_framework import viewsets, mixins
from rest_framework.response import Response

from recipe.models import Ingredient, Recipe, Step, User
from recipe.serializers import RecipeSerializer, UserSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        """
        Return a list of all the users.
        """
        return self.list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Return a user instance.
        """
        if kwargs['username']:
            username = kwargs['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'User could not be found.'}, status=404)
        else:
            return Response({'Bad request.'}, status=400)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipies to be viewed or edited.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'name'

