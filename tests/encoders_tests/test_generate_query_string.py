from decimal import Decimal
from src.QueryStringManager import QueryStringManager

import unittest

class TestGenerateQueryString(unittest.TestCase):
    """
        Tests for :class:`QueryStringManager.generate_query_string()`
    """

    def test_throws_exception_on_invalid_dict(self):
        """
        This method should throw a ValueError if the passed dictionary of params is not a
        valud "single level" dictionary or does not have values that can be written to a 
        query string
        """

        TEST_INVALID_DICTS = [
            None,
            1,
            {"test": {}},
            {"test": None}
        ]

        for test_dict in TEST_INVALID_DICTS:
            self.assertRaises(ValueError, lambda: QueryStringManager.generate_query_string(test_dict))


    def test_creates_single_arg_query_string(self):
        """
        Create a single argument query string from a dict with a single key-value pair
        
        A valid query string will begin with a "?" and use "=" to seperate keys and values, like:
        "?key=value"
        """

        TEST_DICTS_AND_RESULTS = [
            ({"key": "value"}, "?key=value"),
            ({"key w/ sp'ec chars": "value w/ spec chars!"}, "?key%20w/%20sp%27ec%20chars=value%20w/%20spec%20chars!"),
            ({"test": 1}, "?test=1"),
            ({"test": True}, "?test=true"),
            ({"test": False}, "?test=false"),
            ({"test": 3.14}, "?test=3.14"),
            ({"test": Decimal("3.14")}, "?test=3.14"),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[1], QueryStringManager.generate_query_string(test_dict[0]))


    def test_creates_multiple_arg_query_string(self):
        """
        Create a multiple argument query string from a dict with a multiple key-value pairs
        
        A valid query string will begin with a "?" and use "=" to seperate keys and values 
        and "&" to seperate key/value pairs, like:
        "?key=value&key2=value2"
        """

        TEST_DICTS_AND_RESULTS = [
            ({"key": "value", "key2": "value2"}, "?key=value&key2=value2"),
            ({"test": 1, "test2": 3.14}, "?test=1&test2=3.14"),
            ({"test": True, "val2": False}, "?test=true&val2=false"),
            ({"test": -1, "test2": "hello", "test3": False, "test4": 0.01}, "?test=-1&test2=hello&test3=false&test4=0.01"),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[1], QueryStringManager.generate_query_string(test_dict[0]))
    
            
    def test_override_safe_chars(self):
        """
        Test the ability to override the "safe" characters to not replace with URL safe notations in a query string
        This can be done by passing a string containg all characters that should not be replaced as an optional
        parameter of `generate_query_string()`
        """

        TEST_DICTS__RULES_AND_RESULTS = [
            (" /'!=", {"key w/ sp'ec chars": "value w/ spec chars!"}, "?key w/ sp'ec chars=value w/ spec chars!"),
            ("/'!=", {"key w/ sp'ec chars": "value w/ spec chars!"}, "?key%20w/%20sp'ec%20chars=value%20w/%20spec%20chars!"),
            ("/'!", {"key w/ sp'ec chars": "value w/ spec chars!"}, "?key%20w/%20sp'ec%20chars%3Dvalue%20w/%20spec%20chars!"),
        ]

        for test_dict in TEST_DICTS__RULES_AND_RESULTS:
            self.assertEqual(test_dict[2], QueryStringManager.generate_query_string(test_dict[1], test_dict[0]))
