from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from recipes.validators import RecipeValidator
from tag.serializers import TagSerializer
from tag.models import Tag

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import Response


@api_view(http_method_names=['GET', 'POST'])
def recipes_api_list(req):
    if req.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': req}
        )
        return Response(serializer.data)
    elif req.method == 'POST':
        serializer = RecipeSerializer(
            data=req.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view()
def recipes_api_detail(req, pk):
    recipe = Recipe.objects.get_published().filter(pk=pk).first()
    if not recipe:
        return Response({
            'error_message': 'Recipe not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeSerializer(
        instance=recipe,
        context={'request': req}
    )
    return Response(serializer.data)


@api_view()
def tags_api_detail(req, pk):
    tag = Tag.objects.filter(pk=pk).first()
    if not tag:
        return Response({
            'error_message': 'Tag not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)