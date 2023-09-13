from unittest import TestCase
from pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=1)
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_first_range_is_static_if_current_page_is_shorter_than_the_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=1)
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_range_changes_if_larger_than_the_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=3)
        self.assertEqual([2, 3, 4, 5], pagination['pagination'])

    def test_range_is_static_if_near_last_page(self):
        # The range only changes if is at third to last page.
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=18)
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=19)
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=20)
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])
