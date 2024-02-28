import os

from PIL import Image
from PIL.Image import Resampling

from tag.models import Tag

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import F, Value, QuerySet
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.functions import Concat


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_published(self) -> QuerySet:
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('user__first_name'),
                Value(' '),
                F('user__last_name'),
                Value(' ('),
                F('user__username'),
                Value(')'),
            ),
        ).order_by('-id').select_related(
            'category',
            'user').prefetch_related('tags')


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(
        max_length=150,
        verbose_name=_('Description'))
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(
        verbose_name=_('Preparation time')
    )
    preparation_time_unit = models.CharField(
        max_length=65,
        verbose_name=_('Preparation time unit')
    )
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(
        max_length=65,
        verbose_name=_('Servings unit')
    )
    preparation_steps = models.TextField(verbose_name=_('Preparation steps'))
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/',
        blank=True,
        default='',
        verbose_name=_('Cover')
    )
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL, null=True,
                                 blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(to=Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def resize_cover(self, new_width):
        img_full_path = os.path.join(settings.MEDIA_ROOT, self.cover.name)
        tmp_cover = Image.open(img_full_path)
        width, height = tmp_cover.size
        if width <= new_width:
            tmp_cover.close()
            return
        new_height = round((new_width * height) / width)
        new_cover = tmp_cover.resize(
            (new_width, new_height),
            Resampling.BICUBIC
        )
        new_cover.save(
            img_full_path,
            optimize=True,
            quality=50,
        )

    def get_absolute_url(self):
        return reverse('recipes:detail', args=(self.pk,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()
        if recipe_from_db is not None and recipe_from_db.pk != self.pk:
            raise ValidationError({
                'title': ValidationError(
                    message='A recipe with this title already exists, ' +
                    'try another one.',
                    code='invalid'
                )
            })
