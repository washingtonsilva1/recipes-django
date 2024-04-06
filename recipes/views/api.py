from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from recipes.permissions import IsOwner
from tag.serializers import TagSerializer
from tag.models import Tag

from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category_id', '')
        if category_id and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner()]
        return super().get_permissions()

    def partial_update(self, req, *args, **kwargs):
        recipe = self.get_object()
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


@ api_view()
def tags_api_detail(req, pk):
    tag = Tag.objects.filter(pk=pk).first()
    if not tag:
        return Response({
            'error_message': 'Tag not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
