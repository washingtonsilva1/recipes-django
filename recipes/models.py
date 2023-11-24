from tag.models import Tag

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL, null=True,
                                 blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(to=Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:detail', args=(self.pk,))

    def clean(self):
        cleaned_data = super().clean()
        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()
        if recipe_from_db and recipe_from_db.pk != self.pk:
            raise ValidationError({
                'title': ValidationError(
                    message='A recipe with this title already exists, ' +
                    'try another one.',
                    code='invalid'
                )
            })
        return cleaned_data

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
