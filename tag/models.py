from utils.utils import generate_random_string
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            r = generate_random_string()
            self.slug = slugify(f'{self.name} {r}')
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.name
