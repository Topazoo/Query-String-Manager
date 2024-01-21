from src.QueryStringManager import QueryStringManager

import unittest

# Typing
from decimal import Decimal

class TestUnifiedParseQueryString(unittest.TestCase):
    """
        Tests for :class:`QueryStringManager.parse()` which will automatically detect the format of the query string
    """

    def test_parse_single_arg_query_string_normal_format(self):
        """
        Parse a single argument query string to a dict with a single key-value pair
        
        A valid query string will begin with a "?" and use "=" to seperate keys and values, like:
        "?key=value"
        """

        TEST_DICTS_AND_RESULTS = [
            ({"key": "usb"}, "?key=usb"),
            ({"key": "==usb="}, "?key===usb="),
            ({"key": "value="}, "?key=value="),
            ({"key": "value"}, "?key=value"),
            ({"key w/ sp'ec chars": "value w/ spec chars!"}, "?key%20w/%20sp%27ec%20chars=value%20w/%20spec%20chars!"),
            ({"test": 1}, "?test=1"),
            ({"test": True}, "?test=true"),
            ({"test": False}, "?test=false"),
            ({"test": Decimal("3.14")}, "?test=3.14"),
            ({"test": "MSFT"}, "?test=MSFT")
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[0], QueryStringManager.parse(test_dict[1]))


    def test_parse_multiple_arg_query_string_normal_format(self):
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
            self.assertEqual(test_dict[0], QueryStringManager.parse(test_dict[1]))
    
            
    def test_parse_single_arg_query_string_base64(self):
        """
        Parse a base64 encoded query string to a dict with a single key-value pair
        """

        TEST_DICTS_AND_RESULTS = [
            ({"q": {"key": "value"}}, "?q=eyJrZXkiOiAidmFsdWUifQ=="),
            ({"field": {"key": "value"}}, "field=eyJrZXkiOiAidmFsdWUifQ=="),
            ({"field name": {"key w/ sp'ec chars": "value w/ spec chars!"}}, "?field%20name=eyJrZXkgdy8gc3AnZWMgY2hhcnMiOiAidmFsdWUgdy8gc3BlYyBjaGFycyEifQ=="),
            ({"1": {"test": {"nested": 1}}}, "?1=eyJ0ZXN0IjogeyJuZXN0ZWQiOiAxfX0="),
            ({"q": {"test": [1,2,3]}}, "?q=eyJ0ZXN0IjogWzEsIDIsIDNdfQ=="),
            ({"1": {"test": [{"hi": "There"}]}}, "?1=eyJ0ZXN0IjogW3siaGkiOiAiVGhlcmUifV19"),
            ({"q": {"test": Decimal("3.14")}}, "?q=eyJ0ZXN0IjogMy4xNH0="),
            ({"q": {"test": "3.14"}}, "?q=eyJ0ZXN0IjogIjMuMTQifQ=="),
            ({"q": {"test": Decimal("3.14")}}, "?q=eyJ0ZXN0IjogMy4xNH0="),
            ({"=": {"test": [True]}}, "?%3D=eyJ0ZXN0IjogW3RydWVdfQ=="),
            ({"q": "Hello"}, "?q=IkhlbGxvIg=="),
            ({"test": [1,2,3]}, "?test=WzEsIDIsIDNd"),
            ({"field name": Decimal("0.01")}, "?field%20name=MC4wMQ=="),
            ({"test": Decimal("3.14")}, "?test=My4xNA=="),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[0], QueryStringManager.parse(test_dict[1]))


    def test_parse_multiple_arg_query_string_base64(self):
        """
        Parse a base64 encoded query string to a dict with multiple key-value pairs
        """

        TEST_DICTS_AND_RESULTS = [
            ({"q": {"key": "value", "1": "5"}, "field": {"key": "value"}}, "?q=eyJrZXkiOiAidmFsdWUiLCAiMSI6ICI1In0=&field=eyJrZXkiOiAidmFsdWUifQ=="),
            ({"t": {"key w/ sp'ec chars": "value w/ spec chars!"}, "y": {"test2": [1,2,3]}}, "?t=eyJrZXkgdy8gc3AnZWMgY2hhcnMiOiAidmFsdWUgdy8gc3BlYyBjaGFycyEifQ==&y=eyJ0ZXN0MiI6IFsxLCAyLCAzXX0="),
            ({"hello world": {"test": {"nested": 1}, "test2": [{"hi": "There"}], "test3": Decimal("3.14")}}, "?hello%20world=eyJ0ZXN0IjogeyJuZXN0ZWQiOiAxfSwgInRlc3QyIjogW3siaGkiOiAiVGhlcmUifV0sICJ0ZXN0MyI6IDMuMTR9"),
            ({"test": [1,2,3], "field name": "0.1"}, "?test=WzEsIDIsIDNd&field%20name=IjAuMSI="),
            ({"q": "Hello", "=": True}, "?q=IkhlbGxvIg==&==dHJ1ZQ=="),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[0], QueryStringManager.parse(test_dict[1]))

            
    def test_parse_multiple_arg_query_string_mixed_format(self):
        """
        Parse a mixed base64 and standard format query string to a dict with multiple key-value pairs
        """

        TEST_DICTS_AND_RESULTS = [
            ({"q": {"key": "value", "1": "5"}, "test2": Decimal("-3.14")}, "?q=eyJrZXkiOiAidmFsdWUiLCAiMSI6ICI1In0=&test2=-3.14"),
            ({"val2": False, "y": {"test2": [1,2,3]}}, "?val2=false&y=eyJ0ZXN0MiI6IFsxLCAyLCAzXX0="),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[0], QueryStringManager.parse(test_dict[1]))