import requests
from linkedin_api.common.constants import RESTLI_METHODS, CONTENT_TYPE, HTTP_METHODS, RESTLI_METHOD_TO_HTTP_METHOD_MAP, HEADERS
import linkedin_api.clients.restli.utils.api as apiutils
import random
import string
import json
from typing import Optional, Type

MAX_QUERY_STRING_LENGTH = 4000


def is_query_tunneling_required(encoded_query_param_string):
    return encoded_query_param_string and len(encoded_query_param_string) > MAX_QUERY_STRING_LENGTH


def maybe_apply_query_tunneling_get_requests(*, url: str, encoded_query_param_string: Optional[str] = None, original_restli_method: RESTLI_METHODS, access_token, version_string):
    if is_query_tunneling_required(encoded_query_param_string):
        request = requests.Request(
            method=HTTP_METHODS.POST.value,
            url=url,
            data=encoded_query_param_string,
            headers=apiutils.get_restli_request_headers(
                content_type=CONTENT_TYPE.URL_ENCODED.value,
                http_method_override=HTTP_METHODS.GET.value,
                restli_method=original_restli_method,
                access_token=access_token,
                version_string=version_string
            )
        )
    else:
        url = f"{url}?{encoded_query_param_string}" if encoded_query_param_string else url
        request = requests.Request(
            method=RESTLI_METHOD_TO_HTTP_METHOD_MAP[original_restli_method.value.upper(
            )],
            url=url,
            headers=apiutils.get_restli_request_headers(
                restli_method=original_restli_method,
                access_token=access_token,
                version_string=version_string
            )
        )
    return request.prepare()

def maybe_apply_query_tunneling_requests_with_body(*,
                                                   encoded_query_param_string: Optional[str],
                                                   url,
                                                   original_restli_method: RESTLI_METHODS,
                                                   original_request_body,
                                                   access_token,
                                                   version_string
                                                   ):
    original_http_method = RESTLI_METHOD_TO_HTTP_METHOD_MAP[original_restli_method.value.upper(
    )]

    if encoded_query_param_string and is_query_tunneling_required(encoded_query_param_string):
        boundary = generate_random_string()
        raw_request_body_string = encoded_query_param_string + \
            json.dumps(original_request_body)
        while raw_request_body_string.find(boundary) >= 0:
            boundary = generate_random_string()

        multipart_request_body = (
            f"--{boundary}\r\n"
            f"{HEADERS.CONTENT_TYPE.value}: {CONTENT_TYPE.URL_ENCODED.value}\r\n\r\n"
            f"{encoded_query_param_string}\r\n"
            f"--{boundary}\r\n"
            f"{HEADERS.CONTENT_TYPE.value}: {CONTENT_TYPE.JSON.value}\r\n\r\n"
            f"{json.dumps(original_request_body)}\r\n"
            f"--{boundary}--"
        )

        request = requests.Request(
            method=HTTP_METHODS.POST.value,
            url=url,
            data=multipart_request_body,
            headers=apiutils.get_restli_request_headers(
                content_type=CONTENT_TYPE.MULTIPART_MIXED_WITH_BOUNDARY.value(
                    boundary),
                http_method_override=original_http_method,
                restli_method=original_restli_method,
                access_token=access_token,
                version_string=version_string
            )
        )
    else:
        final_url = f"{url}?{encoded_query_param_string}" if encoded_query_param_string else url

        request = requests.Request(
            method=original_http_method,
            url=final_url,
            json=original_request_body,
            headers=apiutils.get_restli_request_headers(
                restli_method=original_restli_method,
                access_token=access_token,
                version_string=version_string
            )
        )
    return request.prepare()


def generate_random_string():
    return ''.join(random.choices(string.ascii_letters, k=10))
