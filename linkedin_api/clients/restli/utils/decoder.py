from linkedin_api.common.errors import InvalidSerializedRestliError
from linkedin_api.common.constants import (
    LIST_PREFIX,
    LIST_SUFFIX,
    LIST_ITEM_SEP,
    OBJ_PREFIX,
    OBJ_SUFFIX,
    OBJ_KEY_VAL_SEP,
    OBJ_KEY_VAL_PAIR_SEP,
    LEFT_BRACKET,
    RIGHT_BRACKET,
)
from urllib.parse import unquote
from typing import Dict, List, Any, Union
import re

# These special characters are URL-encoded in reduced encoded primitives: "(", ")", ",", ":", "'"
reduced_decode_special_chars_pattern = r"%28|%29|%2C|%3A|%27"


def decode(value: str) -> Union[Dict[str, Any], List[Any], str]:
    """
    Entry point to decode a Rest.li URL-encoded value. Note that the Rest.li format is lossy since all
    values come out as strings. For example:
    [1,2,3] -encode-> "List(1,2,3)" -decode-> ["1","2","3"]

    Args:
        value (str): The URL-encoded value to decode

    Returns:
        Union[Dict[str,Any], List[Any], str]: The decoded value
    """
    return __internal_decode(value, False)


def reduced_decode(value: str) -> Union[Dict[str, Any], List[Any], str]:
    """
    Entry point to perform reduced decode of a Rest.li HTTP body/header-encoded value.

    Args:
        value (str): The HTTP body/header-encoded value to decode

    Returns:
        Union[Dict[str,Any], List[Any], str]: The decoded value
    """
    return __internal_decode(value, True)


def __validateSuffix(restli_encoded_str: str, suffix: str):
    """
    Validates that the input restli_encoded_str has the expected suffix at the end
    """
    if not restli_encoded_str.endswith(suffix):
        raise InvalidSerializedRestliError(
            f"The serialized Rest.li string has unbalanced prefix and suffix: {restli_encoded_str}"
        )


def __restli_unescape(value: str, reduced: bool):
    if not reduced:
        value = unquote(value)
    elif re.search(reduced_decode_special_chars_pattern, value):
        value = re.sub(
            reduced_decode_special_chars_pattern,
            lambda match: unquote(match.group()),
            value,
        )
    return value


def __find_last_right_bracket(value: str, pos: int) -> int:
    """
    Returns the index of the last right, matching bracket, starting from specified index.
    For example, consider value = "List(1,(k:v))".
    If pos = 0, then return the position of the outer matching bracket (12)
    If pos = 7, then return the position of the inner matching bracket (11)

    Args:
        value (str): The encoded string value
        pos (int): The index at which to start searching

    Raises:
        InvalidSerializedRestliError: Exception if there are unmatched brackets

    Returns:
        int: The index of the right matching bracket
    """
    unmatched_brackets = 0
    # Keep track of if we have encountered at least one left bracket
    has_met_first = False
    idx = pos

    while idx < len(value):
        # Iterate through the string, if find left bracket, add to unmatched_brackets.
        # If you find right brackets, decrement unmatched_brackets
        # Once there are 0 unmatched brackets left, break
        curr_char = value[idx]
        if curr_char == LEFT_BRACKET:
            unmatched_brackets += 1
            has_met_first = True
        if curr_char == RIGHT_BRACKET:
            unmatched_brackets -= 1
        if unmatched_brackets == 0 and has_met_first:
            break
        idx += 1
    if unmatched_brackets > 0:
        # We have unmatched brackets, so throw error
        raise InvalidSerializedRestliError(
            f"The serialized Rest.li string has unbalanced brackets: {value}"
        )
    return idx


def __internal_decode(restli_encoded_str: str, reduced: bool):
    if (restli_encoded_str is None) or (restli_encoded_str == "''"):
        restli_encoded_str = ""

    if restli_encoded_str.startswith(LIST_PREFIX):
        __validateSuffix(restli_encoded_str, LIST_SUFFIX)
        return __decode_list(restli_encoded_str[5:-1], reduced)
    elif restli_encoded_str.startswith(OBJ_PREFIX):
        __validateSuffix(restli_encoded_str, OBJ_SUFFIX)
        return __decode_object(restli_encoded_str[1:-1], reduced)
    else:
        return __restli_unescape(restli_encoded_str, reduced)


def __decode_list(restli_encoded_str: str, reduced: bool) -> List[Any]:
    """
    Decodes a Rest.li-encoded string to a list

    Args:
        restli_encoded_str (str): An encoded string value that should represent a list. It is expected
        that this is the string value inside of "List(...)". For example, if the original string is
        "List(val1,val2,val3)", then the string that should be passed into _decode_list() should be
        "val1,val2,val3".
        reduced (bool): Flag whether this is expected to be a reduced-encoded string

    Returns:
        List[Any]: The decoded list
    """

    decoded_list = []
    idx = 0
    while idx < len(restli_encoded_str):
        if (restli_encoded_str[idx:].startswith(LIST_PREFIX)) or (
            restli_encoded_str[idx:].startswith(OBJ_PREFIX)
        ):
            # If we encounter a List or Object as one of the current list's entries, append the decoded value
            right_bracket_idx = __find_last_right_bracket(restli_encoded_str, idx)
            decoded_list.append(
                __internal_decode(
                    restli_encoded_str[idx : right_bracket_idx + 1], reduced
                )
            )

            # Move past the comma (separating list values)
            idx = right_bracket_idx + 2
        else:
            # The current list entry is a primitive
            end_idx = restli_encoded_str.find(LIST_ITEM_SEP, idx)
            if end_idx < 0:
                end_idx = len(restli_encoded_str)
            decoded_list.append(
                __restli_unescape(restli_encoded_str[idx:end_idx], reduced)
            )

            # Move past the comma
            idx = end_idx + 1
    return decoded_list


def __decode_object(restli_encoded_str: str, reduced: bool) -> Dict[str, Any]:
    """
    Decodes a Rest.li-encoded string to an object.

    Args:
        restli_encoded_str (str): An encoded string value that should represent an object. It is expected
        that this is the string value inside of the parentheses. For example, if the original string is
        "(prop1:val,prop2:val2)", then the string that should be passed into _decode_object() should be
        "prop1:val1,prop2:val2".
        reduced (bool): Flag whether this is expected to be a reduced-encoded string

    Returns:
        Dict[str,Any]: The decoded object
    """
    decoded_object = {}
    idx = 0
    while idx < len(restli_encoded_str):
        # Get the key value between the start index and key-val separator (:)
        colon_idx = restli_encoded_str.find(OBJ_KEY_VAL_SEP, idx)
        key = __restli_unescape(restli_encoded_str[idx:colon_idx], reduced)

        # Move to the next character after the colon
        idx = colon_idx + 1

        if (restli_encoded_str[idx:].startswith(LIST_PREFIX)) or (
            restli_encoded_str[idx:].startswith(OBJ_PREFIX)
        ):
            # If we encounter a List or Object as the key's value, decode it
            right_bracket_idx = __find_last_right_bracket(restli_encoded_str, idx)
            decoded_object[key] = __internal_decode(
                restli_encoded_str[idx : right_bracket_idx + 1], reduced
            )

            # Move index past next potential comma (separating obj key-value pairs)
            idx = right_bracket_idx + 2
        else:
            # The key's value is a primitive
            end_idx = restli_encoded_str.find(OBJ_KEY_VAL_PAIR_SEP, idx)
            if end_idx < 0:
                end_idx = len(restli_encoded_str)

            decoded_object[key] = __restli_unescape(
                restli_encoded_str[idx:end_idx], reduced
            )
            # end_idx is the comma index, so move 1 past it
            idx = end_idx + 1
    return decoded_object
