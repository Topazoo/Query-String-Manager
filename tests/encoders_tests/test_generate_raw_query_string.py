from src.QueryStringParser import QueryStringParser

import unittest

class TestGenerateRawQueryString(unittest.TestCase):
    """
        Tests for :class:`QueryStringParser._generate_raw_query_string()`
    """

    def test_throws_exception_on_invalid_dict(self):
        """
        This method should throw a ValueError if the passed dictionary of params is not single level
        or does not have values that can be written to a query string
        """

        pass


    def test_creates_single_arg_query_string(self):
        """
        Create a single argument query string from a dict with a single key-value pair
        
        A valid query string will begin with a "?" and use "=" to seperate keys and values, like:
        "?key=value"
        """

        pass


    def test_creates_multiple_arg_query_string(self):
        """
        Create a multiple argument query string from a dict with a multiple key-value pairs
        
        A valid query string will begin with a "?" and use "=" to seperate keys and values 
        and "&" to seperate key/value pairs, like:
        "?key=value&key2=value2"
        """

        pass


    