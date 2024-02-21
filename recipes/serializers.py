from rest_framework import serializers
from tag.serializers import TagSerializer
from django.contrib.auth.models import User


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=150)
    published = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user'
    )
    tags = TagSerializer(instance='tags', many=True)

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
