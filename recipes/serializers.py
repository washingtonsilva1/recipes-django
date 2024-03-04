from recipes.models import Recipe
from tag.serializers import TagSerializer
from tag.models import Tag
from utils.utils import parse_str_to_int

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
    tags = TagSerializer(
        data=Tag.objects.all(),
        many=True,
        read_only=True,
    )

    def validate(self, attrs):
        print('validando tudo junto')
        validated_data = super().validate(attrs)
        title = validated_data.get('title', '')
        description = validated_data.get('description', '')
        if title and description and \
                description.lower() == title.lower():
            raise serializers.ValidationError(
                'Your description and title can not be the same.'
            )
        return validated_data

    def validate_title(self, value):
        title = value
        if len(title) < 8:
            raise serializers.ValidationError(
                'Your title must have at least 8 characters.'
            )
        recipe_from_db = Recipe.objects.filter(
            title__iexact=title
        ).first()
        if (recipe_from_db and self.instance and
            recipe_from_db.pk != self.instance.pk) or \
                (recipe_from_db and not self.instance):
            raise serializers.ValidationError(
                'A recipe with this title already exists, ' +
                'try another one.'
            )
        return title

    def validate_description(self, value):
        description = value
        if len(description) < 10:
            raise serializers.ValidationError(
                'Your description must have at least 10 characters.'
            )
        return description

    def validate_servings(self, value):
        servings = value
        if parse_str_to_int(servings) < 1:
            raise serializers.ValidationError(
                'Type a number bigger than zero.'
            )
        return servings

    def validate_preparation_time(self, value):
        preparation_time = value
        if parse_str_to_int(preparation_time) < 1:
            raise serializers.ValidationError(
                'Type a number bigger than zero.'
            )
        return preparation_time

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
