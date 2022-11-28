from decimal import Decimal
from src.QueryStringParser import QueryStringParser

import unittest

class TestParseBase64QueryString(unittest.TestCase):
    """
        Tests for :class:`QueryStringParser._parse_base64_encoded_query_string()`
    """

    def test_throws_exception_on_invalid_string(self):
        """
        This method should throw a ValueError if the passed string of params is not valid string, query string or base64
        """

        TEST_INVALID_DICTS = [
            None,
            1,
            "1234",
            "q=1234",
            "?q=1234",
            "?q=eyJrZXkiOiAidmFsdWUifQ"
        ]

        for test_dict in TEST_INVALID_DICTS:
            self.assertRaises(ValueError, lambda: QueryStringParser._parse_base64_encoded_query_string(test_dict))


    def test_parse_single_arg_query_string(self):
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
            ({"=": {"test": [True]}}, "?%3D=eyJ0ZXN0IjogW3RydWVdfQ=="),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEquals(test_dict[0], QueryStringParser._parse_base64_encoded_query_string(test_dict[1]))


    def test_creates_multiple_arg_query_string(self):
        """
        Parse a base64 encoded query string to a dict with multiple key-value pairs
        """

        TEST_DICTS_AND_RESULTS = [
            ({"q": {"key": "value", "1": "5"}, "field": {"key": "value"}}, "?q=eyJrZXkiOiAidmFsdWUiLCAiMSI6ICI1In0=&field=eyJrZXkiOiAidmFsdWUifQ=="),
            ({"t": {"key w/ sp'ec chars": "value w/ spec chars!"}, "y": {"test2": [1,2,3]}}, "?t=eyJrZXkgdy8gc3AnZWMgY2hhcnMiOiAidmFsdWUgdy8gc3BlYyBjaGFycyEifQ==&y=eyJ0ZXN0MiI6IFsxLCAyLCAzXX0="),
            ({"hello world": {"test": {"nested": 1}, "test2": [{"hi": "There"}], "test3": Decimal("3.14")}}, "?hello%20world=eyJ0ZXN0IjogeyJuZXN0ZWQiOiAxfSwgInRlc3QyIjogW3siaGkiOiAiVGhlcmUifV0sICJ0ZXN0MyI6IDMuMTR9"),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEquals(test_dict[0], QueryStringParser._parse_base64_encoded_query_string(test_dict[1]))