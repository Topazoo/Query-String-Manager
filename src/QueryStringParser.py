# Utils
from urllib.parse import quote

# Typing
from typing import Union

class QueryStringParser:
    # Characters that should not be replaced with URL safe equivalents
    # when generating query strings
    URLLIB_SAFE_CHARS = ";/?!:@&=+$,."

    # Encoders
    def generate_query_string(params:dict, base64_encode:bool) -> str:
        pass

    def _generate_base64_encoded_query_string(params:dict) -> str:
        pass

    def _generate_raw_query_string(params:dict) -> str:
        """
        Generate a query string from a passed dictionary The passed dictionary must 
        meet the conditions defined in `_is_valid_single_level_dict()` or a ValueError will
        be raised

        Arguments:
            params {dict} -- A dictionary of one or more key/value pairs to create a query string with

        Raises:
            ValueError: If the dictionary does not meet the criteria in `_is_valid_single_level_dict()`

        Returns:
            str -- A normalized query string generated from the passed dictionary
        """

        if not QueryStringParser._is_valid_single_level_dict(params):
            raise ValueError("Cannot generate a query string from passed dictionary. \
                Passed data contains a nested dictionary, a list or an datatype that is not \
                (int, float, bool, str)")

        # Create query string and convert booleans to lowercase
        raw_query_string = "&".join([f"{key}={QueryStringParser._normalize_value(value)}" for (key,value) in params.items()])

        # Normalize special characters for URLs
        return "?" + quote(raw_query_string, safe=QueryStringParser.URLLIB_SAFE_CHARS)


    # Decoders
    def parse_query_string(query_string:str) -> dict:
        pass

    def _parse_base64_encoded_query_string(query_string:str) -> dict:
        pass

    def _parse_raw_query_string(query_string:str) -> dict:
        pass
    

    # Utils
    def _is_valid_single_level_dict(params:dict) -> bool:
        """
        Determines if a passed dictionary is "single level." In this context "single level"
        means that this is not a nested dictionary and the values are JSON compatible
        (int, float, bool, str)

        Arguments:
            params {dict} -- The dictionary to check

        Returns:
            bool -- True if the dictionary is single level with valid values. False if 
            it is not single level, does not have valid values or is not a dictionary.
        """
        
        # Ensure dictionary that is not empty
        if not isinstance(params, dict) or len(params) == 0:
            return False

        # Check all values to ensure they're not lists, dictionaries or None
        for value in params.values():
            if not isinstance(value, (float, int, str, bool)):
                return False
            
        return True
    

    def _normalize_value(param:Union[int, str, bool, float]) -> str:
        """
        Normalizes a value for usage in a query string. For the following value types the
        following normalization occurs:

        - str - None
        - int - Converted to a string
        - float - Converted to a string
        - bool - Converted to a lowercase string

        Arguments:
            param {Union[int, str, bool, float]} -- The parameter to normalize

        Returns:
            str -- The normalized value
        """
        
        if isinstance(param, bool):
            return str(param).lower()
        
        return param
