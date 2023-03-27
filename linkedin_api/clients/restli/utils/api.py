import linkedin_api.common.constants as constants
from importlib.metadata import version
from linkedin_api.clients.restli.utils.encoder import encode
from typing import Dict, Any, Optional
from linkedin_api.common.errors import InvalidArgumentError
import re

__version__ = version("linkedin-api-client")


def get_rest_api_base_url(version_string):
    if version_string:
        return constants.VERSIONED_BASE_URL
    else:
        return constants.NON_VERSIONED_BASE_URL


def get_restli_request_headers(
    *,
    restli_method: constants.RESTLI_METHODS,
    access_token,
    version_string=None,
    http_method_override=None,
    content_type="application/json",
):
    headers = {
        "Connection": "Keep-Alive",
        "X-RestLi-Protocol-Version": "2.0.0",
        "X-RestLi-Method": restli_method.value,
        "Authorization": "Bearer " + access_token,
        "Content-Type": content_type,
        "User-Agent": f"linkedin-api-python-client/{__version__}",
    }
    if version_string is not None:
        headers.update({"LinkedIn-Version": version_string})
    if http_method_override is not None:
        headers.update({"X-HTTP-Method-Override": http_method_override})

    return headers


def build_rest_url(
    resource_path: str, path_keys: Optional[Dict[str, Any]] = None, version_string=None
) -> str:
    """Method to build the URL (not including query parameters) for a REST-based API call to LinkedIn.

    Args:
        resource_path (str): The resource path template string, beginning with a forward slash.
          Path key placeholders (if any) should be specified using curly-braces, and the placeholders
          must match the keys defined in the 'path_keys' argument. Examples: `/me` or `/adAccounts/{adAccountId}`
          or `/socialActions/{id}/comments/{commentId}`
        path_keys (Dict[str,Any], optional): Optional path keys dictionary whose keys should map to the
          placeholder values in the 'resource_path' argument. The path keys may be complex keys (objects),
          which will be properly encoded by this method. For example: `{"id": 123, "subId": 456}` or
          `{"complexKey": {"key1": "urn:li:foobar:123", "key2": "urn:li:barbaz:456"}}`. Defaults to None.
        version_string (_type_, optional): Optional version string to be provided if versioned APIs are being used.
          Defaults to None.

    Raises:
        InvalidArgumentError: Error if placeholders in 'resource_path' don't match 'path_keys'

    Returns:
        str: The constructed URL of the API request, not including query parameters
    """

    if version_string:
        base_url = constants.VERSIONED_BASE_URL
    else:
        base_url = constants.NON_VERSIONED_BASE_URL

    # Validate resource_path and path_keys
    num_path_keys = 0 if path_keys == None else len(path_keys.keys())
    if path_keys:
        encoded_path_keys = {k: encode(v) for (k, v) in path_keys.items()}
    else:
        encoded_path_keys = {}

    placeholders = re.findall(r"{(.*?)}", resource_path)

    if len(placeholders) != num_path_keys:
        raise InvalidArgumentError(
            "The number of placeholders in the 'resource_path' argument do not match the number of keys in the 'path_keys' argument"
        )

    try:
        resource_path = resource_path.format(**encoded_path_keys)
    except Exception as error:
        raise InvalidArgumentError(
            "The placeholders in the 'resource_path' argument do not match the keys in the 'path_keys' argument"
        ) from error

    return f"{base_url}{resource_path}"
