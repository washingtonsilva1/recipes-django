import os
from recipes.models import Recipe

from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Recipe)
def recipe_delete_cover(sender, instance, *args, **kwargs):
    db_instance = Recipe.objects.filter(pk=instance.pk).first()
    delete_cover(db_instance)


@receiver(pre_save, sender=Recipe)
def recipe_updated_cover(sender, instance, *args, **kwargs):
    db_instance = Recipe.objects.filter(pk=instance.pk).first()
    if db_instance and db_instance.cover != instance.cover:
        delete_cover(db_instance)
