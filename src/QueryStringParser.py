class QueryStringParser:

    # Encoders
    def generate_query_string(params:dict, base64_encode:bool) -> str:
        pass

    def _generate_base64_encoded_query_string(params:dict) -> str:
        pass

    def _generate_raw_query_string(params:dict) -> str:
        pass


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


    def _is_base64_encoded(query_string:str) -> bool:
        pass