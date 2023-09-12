from unittest import TestCase
from pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            range=list(range(1, 21)),
            pages=4,
            current=1)
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_shorter_than_the_middle(self):
        pagination = make_pagination_range(
            range=list(range(1, 21)),
            pages=4,
            current=1)
        self.assertEqual([1, 2, 3, 4], pagination)
