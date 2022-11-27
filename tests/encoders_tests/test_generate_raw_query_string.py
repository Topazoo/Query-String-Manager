from src.QueryStringParser import QueryStringParser

import unittest

class TestGenerateRawQueryString(unittest.TestCase):
    """
        Tests for :class:`QueryStringParser._generate_raw_query_string()`
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
            self.assertRaises(ValueError, QueryStringParser._generate_raw_query_string(test_dict))


    def test_creates_single_arg_query_string(self):
        """
        Create a single argument query string from a dict with a single key-value pair
        
        A valid query string will begin with a "?" and use "=" to seperate keys and values, like:
        "?key=value"
        """

        TEST_DICTS_AND_RESULTS = [
            ({"key": "value"}, "?key=value"),
            ({"test": 1}, "?test=1"),
            ({"test": True}, "?test=true"),
            ({"test": False}, "?test=false"),
            ({"test": 3.14}, "?test=3.14"),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEquals(test_dict[1], QueryStringParser._generate_raw_query_string(test_dict[0]))


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
            self.assertEquals(test_dict[1], QueryStringParser._generate_raw_query_string(test_dict[0]))
    