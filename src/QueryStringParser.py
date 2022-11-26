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
    def _is_single_level_dict(params:dict) -> bool:
        pass

    def _is_base64_encoded(query_string:str) -> bool:
        pass