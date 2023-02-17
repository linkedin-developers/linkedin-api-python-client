from linkedin_api.common.constants import OAUTH_BASE_URL
from urllib.parse import urlencode, quote
from typing import Optional


def generate_member_auth_url(
    client_id: str, redirect_url: str, scopes: list, state: Optional[str] = None
):
    if not scopes:
        raise Exception("At least one scope must be specified.")

    query_param_string = urlencode(
        {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_url,
            "scope": " ".join(scopes),
        },
        quote_via=quote,
    )

    if state:
        query_param_string += f"&state={state}"

    return f"{OAUTH_BASE_URL}/authorization?{query_param_string}"
