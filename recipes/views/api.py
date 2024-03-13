from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from tag.serializers import TagSerializer
from tag.models import Tag

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404


class RecipesAPIPagination(PageNumberPagination):
    page_size = 5


class RecipesAPIViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipesAPIPagination

    def get_recipe(self, pk: int) -> Recipe:
        return get_object_or_404(
            Recipe,
            pk=pk
        )

    def partial_update(self, req, *args, **kwargs):
        recipe = self.get_recipe(kwargs.get('pk'))
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            data=self.request.data,
            context={'request': self.request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data
        )


@api_view()
def tags_api_detail(req, pk):
    tag = Tag.objects.filter(pk=pk).first()
    if not tag:
        return Response({
            'error_message': 'Tag not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
