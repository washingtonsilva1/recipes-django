from unittest import TestCase
import pytest
from utils.utils import parse_str_to_list


@pytest.mark.fast
class UtilsTest(TestCase):
    def test_parse_str_to_list_returns_empty_list_if_string_is_empty(self):
        string_to_test = ''
        self.assertEqual(parse_str_to_list(string_to_test, ','), [])
        string_to_test = '  '
        self.assertEqual(parse_str_to_list(string_to_test, ','), [])

    def test_parse_str_to_list_is_using_comma_by_default(self):
        string_to_test = 'a,b,c,d,e'
        sep = 12
        self.assertEqual(
            parse_str_to_list(string_to_test, sep),
            ['a', 'b', 'c', 'd', 'e']
        )
        sep = ''
        self.assertEqual(
            parse_str_to_list(string_to_test, ''),
            ['a', 'b', 'c', 'd', 'e']
        )
        sep = '  '
        self.assertEqual(
            parse_str_to_list(string_to_test, ''),
            ['a', 'b', 'c', 'd', 'e']
        )

    def test_parse_str_to_list_is_removing_blank_spaces_from_strings(self):
        string_to_test = '  a, b , c, d, e    ,'
        self.assertEqual(
            parse_str_to_list(string_to_test, ','),
            ['a', 'b', 'c', 'd', 'e']
        )
        string_to_test = '  a, b , c, d    , e    ,    '
        self.assertEqual(
            parse_str_to_list(string_to_test, ','),
            ['a', 'b', 'c', 'd', 'e']
        )
