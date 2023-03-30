from linkedin_api.common.constants import (
    LIST_PREFIX,
    LIST_SUFFIX,
    LIST_ITEM_SEP,
    OBJ_PREFIX,
    OBJ_SUFFIX,
    OBJ_KEY_VAL_SEP,
    OBJ_KEY_VAL_PAIR_SEP,
)
from typing import Optional, List, Dict, Any, Union
from urllib.parse import quote


def param_encode(raw_query_params_map: Optional[Dict[str, Any]]) -> str:
    """
    Entry point for URI-encoding a map of query parameters and generating the resulting query string.
    This function will encode both keys and values according to the Rest.li encoding protocol.

    Args:
        raw_query_params_map (Optional[Dict[str, Any]]): The unencoded query params dictionary with
        keys being the query parameter names and values being the query parameter values.
        For example: { "param1": "val1", "param2": [1,2], "param3": { "k1": "v1" }

    Returns:
        str: The encoded query string. For example: "param1=val1&param2=List(1,2)&param3=(k1:v1)")
    """
    if raw_query_params_map is None:
        return ""

    query_params_map = __encode_query_param_map(raw_query_params_map)
    return "&".join(
        [f"{key}={query_params_map[key]}" for key in sorted(query_params_map.keys())]
    )


def encode(value: Union[bool, str, int, float, List, Dict]) -> str:
    """
    Entry point for URI-encoding a single value using the Rest.li encoding protocol.

    Args:
        value (Union[bool, str, int, float, List, Dict]): The value to encode

    Returns:
        str: The encoded string representing the input value
    """
    if value is None:
        return ""
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, str):
        return __encode_string(value)
    elif isinstance(value, list):
        return __encode_list(value)
    elif isinstance(value, dict):
        return __encode_dict(value)
    else:
        # Everything else (e.g. int, float)
        return str(value)


def __encode_query_param_map(raw_query_params_map: Dict[str, Any]) -> Dict:
    # Return a Dict with the input keys and values encoded
    return {__encode_string(k): encode(v) for (k, v) in raw_query_params_map.items()}


def __encode_string(value: str) -> str:
    # Perform standard URL-encoding on strings
    return quote(value, safe="")


def __encode_list(value: List[Any]) -> str:
    # Encode a list
    return f"{LIST_PREFIX}{LIST_ITEM_SEP.join(encode(el) for el in value)}{LIST_SUFFIX}"


def __encode_dict(value: Dict[str, Any]) -> str:
    # Encode a dict by encoding both key and value, both of which can be complex
    key_values = OBJ_KEY_VAL_PAIR_SEP.join(
        f"{encode(k)}{OBJ_KEY_VAL_SEP}{encode(v)}" for (k, v) in sorted(value.items())
    )

    return f"{OBJ_PREFIX}{key_values}{OBJ_SUFFIX}"
