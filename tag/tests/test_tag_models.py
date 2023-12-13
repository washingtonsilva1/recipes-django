from django.test import TestCase

from tag.models import Tag
from django.db.utils import IntegrityError


class TagModelsTest(TestCase):
    def make_tag(self, **kwargs):
        return Tag.objects.create(**kwargs)

    def test_tag_slug_needs_to_be_unique(self):
        tag_slug = 'dummy-slug'
        self.make_tag(name='DummyTagOne', slug=tag_slug)
        with self.assertRaises(IntegrityError):
            self.make_tag(name='DummyTagTwo', slug=tag_slug)

    def test_tag_is_generating_slug(self):
        tag_name = 'DummyTag'
        t1 = self.make_tag(name=tag_name)
        self.assertIn(f'{tag_name.lower()}-', t1.slug)
