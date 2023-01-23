from decimal import Decimal
from src.QueryStringManager import QueryStringManager

import unittest

class TestGenerateBase64QueryString(unittest.TestCase):
    """
        Tests for :class:`QueryStringManager.generate_base64_query_string()`
    """

    def test_throws_exception_on_invalid_dict(self):
        """
        This method should throw a ValueError if the passed dictionary of params is not a dictionary
        """

        TEST_INVALID_DICTS = [
            None,
            ValueError
        ]

        for test_dict in TEST_INVALID_DICTS:
            self.assertRaises(ValueError, lambda: QueryStringManager.generate_base64_query_string(test_dict))


    def test_creates_single_arg_query_string(self):
        """
        Create a base64 encoded query string from a dict with a single key-value pair
        """

        TEST_DICTS_AND_RESULTS = [
            ({"key": "value"}, "?q=eyJrZXkiOiAidmFsdWUifQ=="),
            ({"key w/ sp'ec chars": "value w/ spec chars!"}, "?q=eyJrZXkgdy8gc3AnZWMgY2hhcnMiOiAidmFsdWUgdy8gc3BlYyBjaGFycyEifQ=="),
            ({"test": {"nested": 1}}, "?q=eyJ0ZXN0IjogeyJuZXN0ZWQiOiAxfX0="),
            ({"test": [1,2,3]}, "?q=eyJ0ZXN0IjogWzEsIDIsIDNdfQ=="),
            ({"test": [{"hi": "There"}]}, "?q=eyJ0ZXN0IjogW3siaGkiOiAiVGhlcmUifV19"),
            ({"test": 3.14}, "?q=eyJ0ZXN0IjogMy4xNH0="),
            ({"test": Decimal("3.14")}, "?q=eyJ0ZXN0IjogMy4xNH0="),
            ({"test": [True]}, "?q=eyJ0ZXN0IjogW3RydWVdfQ=="),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[1], QueryStringManager.generate_base64_query_string(test_dict[0]))

            
    def test_creates_single_arg_query_string_non_dict(self):
        """
        Create a base64 encoded query string from a non-dict with a single key-value pair
        """

        TEST_DICTS_AND_RESULTS = [
            ("Hello", "?q=IkhlbGxvIg=="),
            ("test", [1,2,3], "?test=WzEsIDIsIDNd"),
            ("field name", Decimal(".1"), "?field%20name=MC4x"),
            ("test", Decimal("3.14"), "?test=My4xNA=="),
            ("test", 3.14, "?test=My4xNA=="),
            ("=", True, "?==dHJ1ZQ=="),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            if len(test_dict) == 2:
                self.assertEqual(test_dict[1], QueryStringManager.generate_base64_query_string(test_dict[0]))
            else:
                self.assertEqual(test_dict[2], QueryStringManager.generate_base64_query_string(test_dict[1], test_dict[0]))


    def test_creates_multiple_arg_query_string(self):
        """
        Create a base64 encoded query string from a dict with multiple single key-value pairs
        """

        TEST_DICTS_AND_RESULTS = [
            ({"key": "value", 1: "5"}, "?q=eyJrZXkiOiAidmFsdWUiLCAiMSI6ICI1In0="),
            ({"key w/ sp'ec chars": "value w/ spec chars!", "test2": [1,2,3]}, "?q=eyJrZXkgdy8gc3AnZWMgY2hhcnMiOiAidmFsdWUgdy8gc3BlYyBjaGFycyEiLCAidGVzdDIiOiBbMSwgMiwgM119"),
            ({"test": {"nested": 1}, "test2": [{"hi": "There"}], "test3": 3.14}, "?q=eyJ0ZXN0IjogeyJuZXN0ZWQiOiAxfSwgInRlc3QyIjogW3siaGkiOiAiVGhlcmUifV0sICJ0ZXN0MyI6IDMuMTR9"),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[1], QueryStringManager.generate_base64_query_string(test_dict[0]))

            
    def test_override_field_name(self):
        """
        Test the ability to override the field name used to store the base64 encoded query string data
        """

        TEST_DICTS__RULES_AND_RESULTS = [
            ("field", {"key": "value"}, "?field=eyJrZXkiOiAidmFsdWUifQ=="),
            ("!!!", {"key w/ sp'ec chars": "value w/ spec chars!"}, "?!!!=eyJrZXkgdy8gc3AnZWMgY2hhcnMiOiAidmFsdWUgdy8gc3BlYyBjaGFycyEifQ=="),
            ("_", {"test": {"nested": 1}}, "?_=eyJ0ZXN0IjogeyJuZXN0ZWQiOiAxfX0="),
        ]

        for test_dict in TEST_DICTS__RULES_AND_RESULTS:
            self.assertEqual(test_dict[2], QueryStringManager.generate_base64_query_string(test_dict[1], test_dict[0]))
