from linkedin_api_client.utils.encoder import param_encode
from typing import Dict, Any
import copy


def encode_query_params_for_get_requests(query_params: Dict[str, Any]) -> str:
    """Encodes query params for HTTP GET requests

    This wrapper function on top of encoder.paramEncode is needed specifically to handle the
    "fields" query parameter for field projections. Although Rest.li protocol version 2.0.0 should
    have supported a query param string like "?fields=List(id,firstName,lastName)" it still requires
    the Rest.li protocol version 1.0.0 format of "?fields=id,firstName,lastName". Thus, if "fields"
    is provided as a query parameter for HTTP GET requests, it should not be encoded like all the other
    parameters.

    Args:
        query_params (Dict[str,Any]): a map of query param names and their corresponding values. The query
        param values should not be encoded.

    Returns:
        str: The encoded query param string
    """
    FIELDS_PARAM = "fields"

    query_params_copy = copy.deepcopy(query_params)
    fields = query_params_copy.pop(
        FIELDS_PARAM) if FIELDS_PARAM in query_params_copy.keys() else None

    encoded_query_param_string = param_encode(query_params)
    if fields:
        encoded_query_param_string = '&'.join(
            encoded_query_param_string, f"{FIELDS_PARAM}={fields}")

    return encoded_query_param_string
