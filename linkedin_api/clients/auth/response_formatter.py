from requests import Response
from linkedin_api.clients.auth.response import (
    AccessToken3LResponse,
    AccessToken2LResponse,
    IntrospectTokenResponse,
    RefreshTokenExchangeResponse,
)
from linkedin_api.clients.common.response_formatter import (
    BaseResponseFormatter,
    wrap_format_exception,
)


class AccessToken3LResponseFormatter(BaseResponseFormatter[AccessToken3LResponse]):
    @classmethod
    @wrap_format_exception
    def format_response(cls, response: Response) -> AccessToken3LResponse:
        json_data = response.json()

        return AccessToken3LResponse(
            status_code=response.status_code,
            url=response.url,
            headers=response.headers,
            response=response,
            access_token=json_data.get("access_token", None),
            expires_in=json_data.get("expires_in", None),
            refresh_token=json_data.get("refresh_token", None),
            refresh_token_expires_in=json_data.get("refresh_token_expires_in", None),
            scope=json_data.get("scope", None),
        )


class AccessToken2LResponseFormatter(BaseResponseFormatter[AccessToken2LResponse]):
    @classmethod
    @wrap_format_exception
    def format_response(cls, response: Response) -> AccessToken2LResponse:
        json_data = response.json()

        return AccessToken2LResponse(
            status_code=response.status_code,
            url=response.url,
            headers=response.headers,
            response=response,
            access_token=json_data.get("access_token", None),
            expires_in=json_data.get("expires_in", None),
        )


class IntrospectTokenResponseFormatter(BaseResponseFormatter[IntrospectTokenResponse]):
    @classmethod
    @wrap_format_exception
    def format_response(cls, response: Response) -> IntrospectTokenResponse:
        json_data = response.json()

        return IntrospectTokenResponse(
            status_code=response.status_code,
            url=response.url,
            headers=response.headers,
            response=response,
            active=json_data.get("active", None),
            auth_type=json_data.get("auth_type", None),
            authorized_at=json_data.get("authorized_at", None),
            client_id=json_data.get("client_id", None),
            created_at=json_data.get("created_at", None),
            expires_at=json_data.get("expires_at", None),
            scope=json_data.get("scope", None),
            status=json_data.get("status", None),
        )


class RefreshTokenExchangeResponseFormatter(
    BaseResponseFormatter[RefreshTokenExchangeResponse]
):
    @classmethod
    @wrap_format_exception
    def format_response(cls, response: Response) -> RefreshTokenExchangeResponse:
        json_data = response.json()

        return RefreshTokenExchangeResponse(
            status_code=response.status_code,
            url=response.url,
            headers=response.headers,
            response=response,
            access_token=json_data.get("access_token", None),
            expires_in=json_data.get("expires_in", None),
            refresh_token=json_data.get("refresh_token", None),
            refresh_token_expires_in=json_data.get("refresh_token_expires_in", None),
        )
