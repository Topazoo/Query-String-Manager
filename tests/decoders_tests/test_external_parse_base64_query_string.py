from decimal import Decimal
from src.QueryStringManager import QueryStringManager

import unittest

class TestParseExternalBase64QueryString(unittest.TestCase):
    """
        Tests for :class:`QueryStringManager.parse_base64_query_string()` on strings generated from
        an external source (e.g. Javascript using `btoa(JSON.stringify(obj))`)
    """

    def test_parse_single_arg_query_string(self):
        """
        Parse a base64 encoded query string to a dict with a single key-value pair
        """

        TEST_DICTS_AND_RESULTS = [
            ({"q": {"a": 'a', "b": 'b'}}, "?q=eyJhIjoiYSIsImIiOiJiIn0="),
            ({"num": 123}, "?num=MTIz"),
            ({"1": [1, 2, 3]}, "?1=WzEsMiwzXQ=="),
            ({"2": False}, "?2=ZmFsc2U="),
            ({"3": True}, "?3=dHJ1ZQ=="),
            ({"4": Decimal(".1")}, "?4=MC4x"),
        ]

        for test_dict in TEST_DICTS_AND_RESULTS:
            self.assertEqual(test_dict[0], QueryStringManager.parse_base64_query_string(test_dict[1]))
