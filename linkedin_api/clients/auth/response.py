from linkedin_api.clients.common.response import BaseResponse


class BaseAuthResponse(BaseResponse):
    pass


class AccessToken3LResponse(BaseAuthResponse):
    def __init__(
        self,
        status_code,
        url,
        headers,
        response,
        access_token,
        expires_in,
        refresh_token,
        refresh_token_expires_in,
        scope,
    ):
        super().__init__(
            status_code=status_code, url=url, headers=headers, response=response
        )
        self.access_token = access_token
        """
      The 3-legged access token.
      """

        self.expires_in = expires_in
        """
      The TTL for the access token, in seconds.
      """

        self.refresh_token = refresh_token
        """
      The refresh token value. Only available if refresh tokens are enabled.
      """

        self.refresh_token_expires_in = refresh_token_expires_in
        """
      The TTL for the refresh token, in seconds. Only available if refresh tokens are enabled.
      """

        self.scope = scope
        """
      A comma-separated list of scopes authorized by the member (e.g. "r_liteprofile,r_ads").
      """


class AccessToken2LResponse(BaseAuthResponse):
    def __init__(self, status_code, url, headers, response, access_token, expires_in):
        super().__init__(
            status_code=status_code, url=url, headers=headers, response=response
        )
        self.access_token = access_token
        """
      The two-legged access token.
      """

        self.expires_in = expires_in
        """
      The TTL of the access token, in seconds.
      """


class IntrospectTokenResponse(BaseAuthResponse):
    def __init__(
        self,
        status_code,
        url,
        headers,
        response,
        active,
        auth_type,
        authorized_at,
        client_id,
        created_at,
        expires_at,
        scope,
        status,
    ):
        super().__init__(
            status_code=status_code, url=url, headers=headers, response=response
        )
        self.active = active
        """
      Boolean flag whether the token is a valid, active token.
      """

        self.auth_type = auth_type
        """
      The auth type of the token ("2L", "3L" or "Enterprise_User")
      """

        self.authorized_at = authorized_at
        """
      Epoch time in seconds, indicating when the token was authorized.
      """

        self.client_id = client_id
        """
      Developer application client ID.
      """

        self.created_at = created_at
        """
      Epoch time in seconds, indicating when this token was originally issued.
      """

        self.expires_at = expires_at
        """
      Epoch time in seconds, indicating when this token will expire.
      """

        self.scope = scope
        """
      A string containing a comma-separated list of scopes associated with this token. This is only returned for 3-legged member tokens.
      """

        self.status = status
        """
      The token status ("revoked", "expired", or "active")
      """


class RefreshTokenExchangeResponse(BaseAuthResponse):
    def __init__(
        self,
        status_code,
        url,
        headers,
        response,
        access_token,
        expires_in,
        refresh_token,
        refresh_token_expires_in,
    ):
        super().__init__(
            status_code=status_code, url=url, headers=headers, response=response
        )
        self.access_token = access_token
        """
    The 3-legged access token.
    """

        self.expires_in = expires_in
        """
    The TTL for the access token, in seconds.
    """

        self.refresh_token = refresh_token
        """
    The refresh token value.
    """

        self.refresh_token_expires_in = refresh_token_expires_in
        """
    The TTL for the refresh token, in seconds.
    """
