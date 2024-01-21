# Utils
from urllib.parse import quote, unquote
import json, base64

# Typing
from typing import Union
from decimal import Decimal

class QueryStringManager:
    # Characters that should not be replaced with URL safe equivalents
    # when generating query strings
    URLLIB_SAFE_CHARS = ";/?!:@&=+$,."

    # ----------------------- Encoders ----------------------- #
    @classmethod
    def generate_base64_query_string(cls, params:Union[int, str, bool, float, Decimal, list, dict], field_name:str="q") -> str:
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

        if not isinstance(params, (int, str, bool, float, Decimal, list, dict)):
            raise ValueError("Cannot generate a base64 encoded query string. Passed params argument is \
            not serializable")
        
        query_string_data = base64.urlsafe_b64encode(json.dumps(params, default=float).encode('UTF-8'))
        return f"?{quote(field_name, safe=cls.URLLIB_SAFE_CHARS)}={query_string_data.decode('UTF-8')}"

    
    @classmethod
    def generate_query_string(cls, params:dict, safe_chars:str=None) -> str:
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

        if not cls._is_valid_single_level_dict(params):
            raise ValueError("Cannot generate a query string from passed dictionary. \
                Passed data contains a nested dictionary, a list or an datatype that is not \
                (int, float, bool, str)")

        # Create query string and convert booleans to lowercase
        raw_query_string = "&".join([f"{key}={cls._normalize_value(value)}" for (key,value) in params.items()])

        # Normalize special characters for URLs
        return "?" + quote(raw_query_string, safe=safe_chars or cls.URLLIB_SAFE_CHARS)
    # -------------------------------------------------------- #

    
    # ----------------------- Decoders ----------------------- #
    @classmethod
    def parse(cls, query_string:str) -> dict:
        """
        Parses a passed query string into a dictionary. The data in the query string may be in standard or
        in base64 format. This method will detect the encoding and parse it. Values parsed from the query string
        will be normalized to Python objects (e.g. "false" will become False). Floating point data will be converted 
        to `decimal.Decimal` to ensure no widening / narrowing issues occur.

        This method can generally be used in place of `parse_base64_query_string()` and `parse_query_string()` with
        the drawback of a slight performance hit checking each the encoding of each field in the query string

        Arguments:
            query_string {str} -- The query string to parse into a dictionary

        Raises:
            ValueError: If the query string is malformatted or invalid

        Returns:
            dict -- The parsed query string
        """

        parsed_data = {}

        # Ensure a string was passed
        if not isinstance(query_string, str):
            raise ValueError("Cannot parse a query string from an object that is not a string")
        
        # Remove "?" if it's at the beginning
        if query_string[0] == "?":
            query_string = query_string[1:]

        # Split fields if multiple fields
        key_value_pairs = query_string.split("&")
        if len(key_value_pairs) < 1:
            raise ValueError("Cannot parse a query string from an empty string")
        
        # Split key and value
        for key_value in key_value_pairs:
            # If the key happens to be "=", handle that
            if key_value[0:2] == "==":
                key_and_value = ["=", key_value.lstrip("=")]
            else:
                key_and_value = key_value.split("=", 1)

            if len(key_and_value) != 2:
                raise ValueError("Malformatted query string")
            
            try:
                parsed_data.update(cls.parse_base64_query_string(key_value))
            except:
                parsed_data.update(cls.parse_query_string(key_value))
        
        return parsed_data

            
    @staticmethod
    def parse_base64_query_string(query_string:str) -> dict:
        """
        Parses a Base64 encoded query string into a dictionary. By default, passed data will be normalized
        to Python objects (e.g. "false" will become False). Floating point data will be converted to `decimal.Decimal`
        to ensure no widening / narrowing issues occur.

        Arguments:
            query_string {str} -- The query string to parse into a dictionary

        Raises:
            ValueError: If the query string is malformatted or invalid

        Returns:
            dict -- The parsed query string
        """
        
        parsed_data = {}

        # Ensure a string was passed
        if not isinstance(query_string, str):
            raise ValueError("Cannot parse a query string from an object that is not a string")
        
        # Remove "?" if it's at the beginning
        if query_string[0] == "?":
            query_string = query_string[1:]

        # Split fields if multiple fields
        key_value_pairs = query_string.split("&")
        if len(key_value_pairs) < 1:
            raise ValueError("Cannot parse a query string from an empty string")
        
        # Split key and value
        for key_value in key_value_pairs:
            # If the key happens to be "=", handle that
            if key_value[0:2] == "==":
                key_and_value = ["=", key_value.lstrip("=")]
            else:
                key_and_value = key_value.split("=", 1)

            if len(key_and_value) != 2:
                raise ValueError("Malformatted query string")
            
            parsed_data[unquote(key_and_value[0])] = json.loads(base64.urlsafe_b64decode(key_and_value[1]), parse_float=lambda flt: Decimal(flt))

        return parsed_data
    
    
    @classmethod
    def parse_query_string(cls, query_string:str, normalize_value:bool=True) -> dict:
        """
        Parses a standard query string into a dictionary. By default, passed data will be normalized
        to Python objects (e.g. "false" will become False). Floating point data will be converted to `decimal.Decimal`
        to ensure no widening / narrowing issues occur.

        Arguments:
            query_string {str} -- The query string to parse into a dictionary

        Keyword Arguments:
            normalize_value {bool} -- If the values parsed should be normalized from strings to Python objects (default: {True})

        Raises:
            ValueError: If the query string is malformatted or invalid

        Returns:
            dict -- The parsed query string
        """

        parsed_data = {}

        # Ensure a string was passed
        if not isinstance(query_string, str):
            raise ValueError("Cannot parse a query string from an object that is not a string")
        
        # Remove "?" if it's at the beginning
        if query_string[0] == "?":
            query_string = query_string[1:]

        # Split fields if multiple fields
        key_value_pairs = query_string.split("&")
        if len(key_value_pairs) < 1:
            raise ValueError("Cannot parse a query string from an empty string")
        
        # Split key and value
        for key_value in key_value_pairs:
            key_and_value = key_value.split("=", 1)

            if len(key_and_value) != 2 or key_and_value[1] == '':
                raise ValueError("Malformatted query string")
            
            # Convert data
            parsed_data[unquote(key_and_value[0])] = cls._un_normalize_value(unquote(key_and_value[1])) if \
                normalize_value else unquote(key_and_value[1])

        return parsed_data
    # -------------------------------------------------------- #

    # -----------------------   Utils  ----------------------- #
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
            if not isinstance(value, (float, int, str, bool, Decimal)):
                return False
            
        return True
    

    @staticmethod
    def _normalize_value(param:Union[int, str, bool, float, Decimal]) -> str:
        """
        Normalizes a value for usage in a query string. For the following value types the
        following normalization occurs:

        - str - None
        - int - Converted to a string
        - float/Decimal - Converted to a string
        - bool - Converted to a lowercase string

        Arguments:
            param {Union[int, str, bool, float]} -- The parameter to normalize

        Returns:
            str -- The normalized value
        """
        
        if isinstance(param, bool):
            return str(param).lower()
        
        return param


    @staticmethod
    def _un_normalize_value(param:str) -> Union[int, str, bool, Decimal]:
        """
        "Un-normalizes" a value passed in a query string. The following datatypes will be
        inferred from the content of the query string and converted to their respective type

        - str - None
        - int - (a detected integer will be converted to an Integer)
        - float - (a detected decimal will be converted to a Decimal)
        - bool - (a value of true/false will be converted to a Python Bool)

        Arguments:
            param {Union[int, str, bool, Decimal]} -- The parameter to "un-normalize"

        Returns:
            str -- The normalized value
        """

        # Check for bool
        if param.lower() in ["false", "true"]:
            return json.loads(param.lower())
        
        # If there is a single . in a series of digits it is a decimal
        if '.' in param and param.replace('.', '1').lstrip('-').isdigit():
            return Decimal(param)

        # If it is all digits but not decimal, it is an integer
        if param.lstrip('-').isdigit():
            return int(param)
        
        return param
    # -------------------------------------------------------- #
