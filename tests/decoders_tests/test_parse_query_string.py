from src.QueryStringManager import QueryStringManager

import unittest

# Typing
from decimal import Decimal

class TestParseQueryString(unittest.TestCase):
    """
        Tests for :class:`QueryStringManager.parse_query_string()`
    """

    def test_throws_exception_on_invalid_query_string(self):
        """
        This method should throw a ValueError if the query string is not formatted correctly
        """

        TEST_INVALID_STRINGS = [
            None,
            1,
            "q=test&data",
            "?q=test&data=",
            "?q="
        ]

        for test_dict in TEST_INVALID_STRINGS:
            self.assertRaises(ValueError, lambda: QueryStringManager.parse_query_string(test_dict))


    def test_parse_single_arg_query_string(self):
        """
        Parse a single argument query string to a dict with a single key-value pair
        
        A valid query string will begin with a "?" and use "=" to seperate keys and values, like:
        "?key=value"
        """

        TEST_DICTS_AND_RESULTS = [
            ({"key": "value"}, "?key=value"),
            ({"key w/ sp'ec chars": "value w/ spec chars!"}, "?key%20w/%20sp%27ec%20chars=value%20w/%20spec%20chars!"),
            ({"test": 1}, "?test=1"),
            ({"test": True}, "?test=true"),
            ({"test": False}, "?test=false"),
            ({"test": Decimal("3.14")}, "?test=3.14"),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[0], QueryStringManager.parse_query_string(test_dict[1]))


    def test_parse_multiple_arg_query_string(self):
        """
        Parse a multiple argument query string to a dict with a multiple key-value pairs
        
        A valid query string will begin with a "?" and use "=" to seperate keys and values 
        and "&" to seperate key/value pairs, like:
        "?key=value&key2=value2"
        """

        TEST_DICTS_AND_RESULTS = [
            ({"key": "value", "key2": "value2"}, "?key=value&key2=value2"),
            ({"test": 1, "test2": Decimal("-3.14")}, "?test=1&test2=-3.14"),
            ({"test": True, "val2": False}, "?test=true&val2=false"),
            ({"test": -1, "test2": "hello", "test3": False, "test4": Decimal(".14")}, "?test=-1&test2=hello&test3=false&test4=.14"),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[0], QueryStringManager.parse_query_string(test_dict[1]))
    
            
    def test_not_normalizing_values(self):
        """
        Test the ability to override the "safe" characters to not replace with URL safe notations in a query string
        This can be done by passing a string containg all characters that should not be replaced as an optional
        parameter of `generate_query_string()`
        """

        TEST_DICTS_AND_RESULTS = [
            ({"key": "value", "key2": "value2"}, "?key=value&key2=value2"),
            ({"test": "1", "test2": "-3.14"}, "?test=1&test2=-3.14"),
            ({"test": "true", "val2": "false"}, "?test=true&val2=false"),
            ({"test": "-1", "test2": "hello", "test3": "false", "test4":".14"}, "?test=-1&test2=hello&test3=false&test4=.14"),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[0], QueryStringManager.parse_query_string(test_dict[1], False))
    