from linkedin_api.clients.restli.utils.decoder import decode, reduced_decode
import pytest


@pytest.mark.parametrize(
    "input_str,expected_output",
    [
        ("", ""),
        ("abc123", "abc123"),
        ("urn%3Ali%20app%3F", "urn:li app?"),
        ("List(1,2,3)", ["1", "2", "3"]),
        ("(key1:val1,key2:val2)", {"key1": "val1", "key2": "val2"}),
        (
            "(key1:urn%3Ali%3Aapp%3A%281%2C2%29,key%3A2:foobar)",
            {"key1": "urn:li:app:(1,2)", "key:2": "foobar"},
        ),
        ("List(abc,def,(key1:val1))", ["abc", "def", {"key1": "val1"}]),
        ("List(List(abc,def),ghi)", [["abc", "def"], "ghi"]),
        (
            "(key1:urn%3Ali%3Adevapp%3A123,key2:List(123%3A456,(key22:abc)))",
            {"key1": "urn:li:devapp:123", "key2": ["123:456", {"key22": "abc"}]},
        ),
    ],
)
def test_decode(input_str: str, expected_output):
    assert decode(input_str) == expected_output


@pytest.mark.parametrize(
    "input_str,expected_output",
    [
        ("", ""),
        ("abc123", "abc123"),
        ("%28urn%29%3Ali%2C_ %3A%27app%3F?", "(urn):li,_ :'app%3F?"),
        ("List(%28a%3Ab%29,%27c%2Cd%27?)", ["(a:b)", "'c,d'?"]),
        ("(a%3Ab?:c%3Ad )", {"a:b?": "c:d "}),
    ],
)
def test_reduced_decode(input_str: str, expected_output):
    assert reduced_decode(input_str) == expected_output
