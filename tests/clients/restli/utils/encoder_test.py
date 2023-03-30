from linkedin_api.clients.restli.utils.encoder import encode, param_encode
from typing import Union, Dict, List, Any
import pytest


@pytest.mark.parametrize(
    "input_value,expected_str",
    [
        (None, ""),
        ("", ""),
        ("abc123", "abc123"),
        (123, "123"),
        (123.5, "123.5"),
        (True, "true"),
        (False, "false"),
        ([1, 2, "foobar"], "List(1,2,foobar)"),
        (
            {"k1": "v1", "k2": "urn:li:app:123", "k3": [1, 2], "k4": {"k41": "foobar"}},
            "(k1:v1,k2:urn%3Ali%3Aapp%3A123,k3:List(1,2),k4:(k41:foobar))",
        ),
        (
            [{"k1": "v1"}, ["v2", " t?':,*!"]],
            "List((k1:v1),List(v2,%20t%3F%27%3A%2C%2A%21))",
        ),
    ],
)
def test_encode(input_value: Union[Dict[str, Any], List[Any], str], expected_str):
    assert encode(input_value) == expected_str


@pytest.mark.parametrize(
    "input_query_params,expected_query_str",
    [
        (None, ""),
        ({"param1": "foobar"}, "param1=foobar"),
        ({"param1": "v1", "param2": "v2"}, "param1=v1&param2=v2"),
        ({"pr op:1": " t?':,*!&+"}, "pr%20op%3A1=%20t%3F%27%3A%2C%2A%21%26%2B"),
        (
            {
                "param1": [{"k1": "v1"}, ["e1", "e2"]],
                "param2": {"k2": {"k21": "v21"}, "k3": ["v3"]},
            },
            "param1=List((k1:v1),List(e1,e2))&param2=(k2:(k21:v21),k3:List(v3))",
        ),
    ],
)
def test_param_encode(input_query_params, expected_query_str):
    assert param_encode(input_query_params) == expected_query_str
