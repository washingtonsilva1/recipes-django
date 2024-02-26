from recipes.models import Recipe
from rest_framework import serializers
from django.contrib.auth.models import User


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'category',
            'preparation',
            'author',
            'published',
            'tags',

        ]

    published = serializers.BooleanField(
        source='is_published',
        read_only=True
    )
    preparation = serializers.SerializerMethodField(
        read_only=True
    )
    category = serializers.StringRelatedField(
        read_only=True
    )
    author = serializers.PrimaryKeyRelatedField(
        source='user',
        read_only=True,
    )
    tags = serializers.HyperlinkedRelatedField(
        view_name='recipes:tags_api_detail',
        many=True,
        read_only=True
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
