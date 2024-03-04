from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from tag.serializers import TagSerializer
from tag.models import Tag

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404


class RecipesAPIPagination(PageNumberPagination):
    page_size = 5


class RecipesAPIListView(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipesAPIPagination

    # def get(self, req, *args, **kwargs):
    #     recipes = Recipe.objects.get_published()[:10]
    #     serializer = RecipeSerializer(
    #         instance=recipes,
    #         many=True,
    #         context={'request': self.request}
    #     )
    #     return Response(serializer.data)

    # def post(self, req, *args, **kwargs):
    #     serializer = RecipeSerializer(
    #         data=self.request.data,
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED
    #     )


class RecipesAPIDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipesAPIPagination
    # def get_recipe(self, pk: int) -> Recipe:
    #     return get_object_or_404(
    #         Recipe,
    #         pk=pk
    #     )

    # def get(self, req, *args, **kwargs):
    #     recipe = self.get_recipe(kwargs.get('pk'))
    #     serializer = RecipeSerializer(
    #         instance=recipe,
    #         context={'request': self.request}
    #     )
    #     return Response(serializer.data)

    # def patch(self, req, *args, **kwargs):
    #     recipe = self.get_recipe(kwargs.get('pk'))
    #     serializer = RecipeSerializer(
    #         instance=recipe,
    #         many=False,
    #         data=req.data,
    #         context={'request': self.request},
    #         partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(
    #         data=serializer.data
    #     )

    # def delete(self, req, *args, **kwargs):
    #     recipe = self.get_recipe(kwargs.get('pk'))
    #     recipe.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def tags_api_detail(req, pk):
    tag = Tag.objects.filter(pk=pk).first()
    if not tag:
        return Response({
            'error_message': 'Tag not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
