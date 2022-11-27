# Utils
from urllib.parse import quote
import json, base64

# Typing
from typing import Union

class QueryStringParser:
    # Characters that should not be replaced with URL safe equivalents
    # when generating query strings
    URLLIB_SAFE_CHARS = ";/?!:@&=+$,."

    @staticmethod
    def generate_base64_encoded_query_string(params:dict, field_name:str="q") -> str:
        """
        Generate a base64 encoded query string from a passed dictionary. Unlike a standard query string,
        a base64 encoded query string can support nested dictionaries and lists. A field identifier should
        be passed to hold the query string (the default is "q"), which produces: "?q=<base64 encoded data"

        Arguments:
            params {dict} -- A dictionary to create a query string from

        Keyword Arguments:
            field_name {str} -- The field name to store the encoded query string data under (default: {"q"})

        Raises:
            ValueError: If the passed value for params is not a dictionary

        Returns:
            str -- The base64 encoded query string
        """

        if not isinstance(params, dict):
            raise ValueError("Cannot generate a base64 encoded query string. Passed params argument is \
            not a dictionary.")
        
        query_string_data = base64.urlsafe_b64encode(json.dumps(params).encode('UTF-8'))
        return f"?{field_name}={query_string_data.decode('UTF-8')}"

    
    @staticmethod
    def generate_query_string(params:dict, safe_chars:str=None) -> str:
        """
        Generate a query string from a passed dictionary The passed dictionary must 
        meet the conditions defined in `_is_valid_single_level_dict()` or a ValueError will
        be raised

        Arguments:
            params {dict} -- A dictionary of one or more key/value pairs to create a query string with
            safe_chars {str} -- An optional string of characters to not replace in a query string. For example
            "!?@="

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
        return "?" + quote(raw_query_string, safe=safe_chars or QueryStringParser.URLLIB_SAFE_CHARS)


    # Decoders
    def parse_query_string(query_string:str) -> dict:
        pass

    def _parse_base64_encoded_query_string(query_string:str) -> dict:
        pass

    def _parse_raw_query_string(query_string:str) -> dict:
        pass
    

    # Utils
    @staticmethod
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
    

    @staticmethod
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
