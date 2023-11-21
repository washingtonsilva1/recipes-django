from random import SystemRandom as sr
import string as st
from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            r = ''.join(
                sr().choices(
                    population=(st.ascii_letters+st.digits),
                    k=5
                )
            )
            self.slug = slugify(f'{self.name} {r}')
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.name
