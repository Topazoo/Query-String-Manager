from src.QueryStringManager import QueryStringManager

import unittest

class TestIsSingleLevelDict(unittest.TestCase):
    """
        Tests for :class:`QueryStringManager._is_valid_single_level_dict()`
    """

    def test_empty_dict_is_invalid(self):
        """
        This library considers empty dictionaries to have no level, so an empty dict is invalid
        """

        test_dict = {}
        is_single_level_dict = QueryStringManager._is_valid_single_level_dict(test_dict)

        self.assertIsNotNone(is_single_level_dict, "This method should never return None")
        self.assertFalse(is_single_level_dict)


    def test_non_dicts_are_invalid(self):
        """
        This library considers non-dictionaries to be invalid
        """

        TEST_NON_DICTS = [
            None,
            1,
            "Hello",
            []
        ]

        for non_dict in TEST_NON_DICTS:
            is_single_level_dict = QueryStringManager._is_valid_single_level_dict(non_dict)
            self.assertIsNotNone(is_single_level_dict, "This method should never return None")
            self.assertFalse(is_single_level_dict)
    
            
    def test_single_level_dict_is_valid(self):
        """
        Test a few single-level dictionaries to ensure they're all valid
        """

        TEST_DICTS = [
            {"test": "val"},
            {"test": "val", "test2": 2, "testPi": 3.14},
            {None: True},
            {1: 2}
        ]

        for test_dict in TEST_DICTS:
            is_single_level_dict = QueryStringManager._is_valid_single_level_dict(test_dict)
            self.assertTrue(is_single_level_dict)


    def test_nested_dict_is_invalid(self):
        """
        Test a few nested dictionaries to ensure they're all invalid
        """

        TEST_DICTS = [
            {"test": {}},
            {"test": {"test": "val"}},
            {None: {}},
        ]

        for test_dict in TEST_DICTS:
            is_single_level_dict = QueryStringManager._is_valid_single_level_dict(test_dict)
            self.assertIsNotNone(is_single_level_dict, "This method should never return None")
            self.assertFalse(is_single_level_dict)


    def test_list_dict_is_invalid(self):
        """
        Test a few dictionaries with lists to ensure they're all invalid
        """

        TEST_DICTS = [
            {"test": []},
            {"test": ["test", "val"]},
            {None: []},
        ]

        for test_dict in TEST_DICTS:
            is_single_level_dict = QueryStringManager._is_valid_single_level_dict(test_dict)
            self.assertIsNotNone(is_single_level_dict, "This method should never return None")
            self.assertFalse(is_single_level_dict)

    def test_none_dict_value_is_invalid(self):
        """
        Test a dictionaries with lists to ensure they're all invalid
        """

        TEST_DICTS = [
            {"test": []},
            {"test": ["test", "val"]},
            {None: []},
        ]

        for test_dict in TEST_DICTS:
            is_single_level_dict = QueryStringManager._is_valid_single_level_dict(test_dict)
            self.assertIsNotNone(is_single_level_dict, "This method should never return None")
            self.assertFalse(is_single_level_dict)