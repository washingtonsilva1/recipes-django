from recipes.models import Recipe
from recipes.validators import RecipeValidator
from rest_framework import serializers


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
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover'

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

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        RecipeValidator(
            data=validated_data,
            errorClass=serializers.ValidationError
        )
        return validated_data

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
