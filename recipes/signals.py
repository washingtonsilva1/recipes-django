import os
from recipes.models import Recipe

from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save, post_save
from django.utils.text import slugify


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Recipe)
def recipe_delete_cover(sender, instance, *args, **kwargs):
    db_instance = Recipe.objects.filter(pk=instance.pk).first()
    if db_instance:
        delete_cover(db_instance)


@receiver(pre_save, sender=Recipe)
def recipe_updated_cover(sender, instance, *args, **kwargs):
    db_instance = Recipe.objects.filter(pk=instance.pk).first()
    if db_instance and db_instance.cover != instance.cover:
        delete_cover(db_instance)


@receiver(post_save, sender=Recipe)
def recipe_resize_cover(sender, instance, created, *args, **kwargs):
    db_instance = Recipe.objects.filter(pk=instance.pk).first()
    if db_instance.cover:
        db_instance.resize_cover(840)


# if the title was changed, then slug will change too
# we can improve this later
@receiver(post_save, sender=Recipe)
def recipe_update_slug(sender, instance, created, *args, **kwargs):
    if not created:
        title_to_slug = instance.title
        instance.slug = slugify(title_to_slug)
