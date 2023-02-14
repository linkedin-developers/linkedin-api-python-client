import requests
from linkedin_api.clients.auth.response_formatter import AccessToken2LResponseFormatter, AccessToken3LResponseFormatter, IntrospectTokenResponseFormatter, RefreshTokenExchangeResponseFormatter
import linkedin_api.common.constants as constants
from linkedin_api.common.errors import MissingArgumentError
import linkedin_api.clients.auth.utils.oauth as oauth
from linkedin_api.clients.auth.response import AccessToken2LResponse, AccessToken3LResponse, IntrospectTokenResponse, RefreshTokenExchangeResponse
from typing import Optional, List
from linkedin_api.common.constants import HTTP_METHODS

class AuthClient:
  """
  A client for making LinkedIn auth-related calls.

  Attributes:
      client_id (str): The client ID of the developer application.
      client_secret (str): The client secret of the developer application.
      redirect_url (Optional[str], optional): The redirect URL. This URL is used in the authorization code flow (3-legged OAuth). Users will be redirected to this URL after authorization. Defaults to None.
      session (requests.Session): The session instance used to make requests to the Auth server. Session attributes can be modified, which will affect all requests.
  """
  def __init__(self, client_id: str, client_secret: str, redirect_url: Optional[str] = None):
    """
    The constructor for the AuthClient class.

    Args:
        client_id (str): The client ID of the developer application.
        client_secret (str): The client secret of the developer application.
        redirect_url (Optional[str], optional): The redirect URL. This URL is used in the authorization code flow (3-legged OAuth). Users will be redirected to this URL after authorization. Defaults to None.
    """
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_url = redirect_url
    self.session = requests.Session()


  def generate_member_auth_url(self, scopes: List[str], state: Optional[str] = None) -> str:
    """
    Generates the member authorization URL to direct members to. Once redirected, the member will be
    presented with LinkedIn's OAuth consent page showing the OAuth scopes your application is requesting
    on behalf of the user.

    Args:
        scopes (List[str]): An array of OAuth scopes (3-legged member permissions) your application is requesting on behalf of the user.
        state (Optional[str], optional): An optional string that can be provided to test against CSRF attacks. Defaults to None.

    Raises:
        MissingArgumentError: Error raised if the auth client was not initialized with a redirect URL, which
        is required for this call.

    Returns:
        str: The member authorization URL

    Example:
        >>> oauth_url = auth_client.generate_member_auth_url(
                scopes=["r_liteprofile", "rw_ads"],
                state="abc123"
            )
    """
    if self.redirect_url is None:
      raise MissingArgumentError("The redirect_url is missing from the AuthClient.")

    return oauth.generate_member_auth_url(
      client_id = self.client_id,
      redirect_url = self.redirect_url,
      scopes = scopes,
      state = state
    )

  def exchange_auth_code_for_access_token(self, code: str) -> AccessToken3LResponse:
    """
    Exchanges an authorization code for a 3-legged access token. After member authorization,
    the browser redirects to the provided redirect URL, setting the authorization code on the
    `code` query parameter.

    Args:
        code (str): The authorization code to exchange for an access token

    Returns:
        AccessToken3LResponse: An instance of the AccessToken3LResponse class representing the
        3-legged access token response details.

    Example:
        >>> response = auth_client.exchange_auth_code_for_access_token(code=my_auth_code)
        >>> access_token = response.access_token
    """

    url = f"{constants.OAUTH_BASE_URL}/accessToken"
    headers = {
      constants.HEADERS.CONTENT_TYPE.value: constants.CONTENT_TYPE.URL_ENCODED.value
    }
    data = {
      "grant_type": "authorization_code",
      "code": code,
      "client_id": self.client_id,
      "client_secret": self.client_secret,
      "redirect_uri": self.redirect_url
    }

    request = requests.Request(method=HTTP_METHODS.POST.value, url=url, data=data, headers=headers)
    prepared_request = request.prepare()
    response = self.session.send(prepared_request)

    return AccessToken3LResponseFormatter.format_response(response)

  def exchange_refresh_token_for_access_token(self, refresh_token: str) -> RefreshTokenExchangeResponse:
    """
    Exchanges a refresh token for a new 3-legged access token. This allows access tokens to be refreshed
    without having the member reauthorize your application. Refresh tokens must be enabled for your
    application.

    Args:
        refresh_token (str): The refresh token to exchange for an access token.

    Returns:
        RefreshTokenExchangeResponse: An instance of RefreshTokenExchangeResponse representing the
        refresh token response details.

    Example:
        >>> response = auth_client.exchange_refresh_token_for_access_token(refresh_token=MY_REFRESH_TOKEN)
        >>> access_token = response.access_token
    """
    url = f"{constants.OAUTH_BASE_URL}/accessToken"
    headers = {
      constants.HEADERS.CONTENT_TYPE.value: constants.CONTENT_TYPE.URL_ENCODED.value
    }
    data = {
      "grant_type": "refresh_token",
      "refresh_token": refresh_token,
      "client_id": self.client_id,
      "client_secret": self.client_secret,
    }

    request = requests.Request(method=HTTP_METHODS.POST.value, url=url, headers=headers, data=data)
    prepared_request = request.prepare()
    response = self.session.send(prepared_request)
    return RefreshTokenExchangeResponseFormatter.format_response(response)

  def get_two_legged_access_token(self) -> AccessToken2LResponse:
    """
    Use client credential flow (2-legged OAuth) to retrieve a 2-legged access token for accessing
    APIs that are not member-specific. Developer applications do not have the client credentials
    flow enabled by default.

    Returns:
        AccessToken2LResponse: An instance of AccessToken2LResponse class representing the two-legged
        access token response

    Example:
        >>> token_response = auth_client.get_two_legged_access_token()
        >>> access_token = token_response.access_token
    """
    url = f"{constants.OAUTH_BASE_URL}/accessToken"
    headers={
      constants.HEADERS.CONTENT_TYPE.value: constants.CONTENT_TYPE.URL_ENCODED.value
    }
    data = {
      'grant_type': 'client_credentials',
      'client_id': self.client_id,
      'client_secret': self.client_secret
    }

    request = requests.Request(method=HTTP_METHODS.POST.value, url=url, headers=headers, data=data)
    prepared_request = request.prepare()
    response = self.session.send(prepared_request)
    return AccessToken2LResponseFormatter.format_response(response)

  def introspect_access_token(self, access_token: str) -> IntrospectTokenResponse:
    """
    Introspect a 2-legged, 3-legged or Enterprise access token to get information on status,
    expiry, and other details.

    Args:
        access_token (str): A 2-legged, 3-legged or Enterprise access token.

    Returns:
        IntrospectTokenResponse: An instance of IntrospectTokenResponse class representing the
        token introspection details

    Example:
        >>> response = auth_client.introspect_access_token(access_token=MY_ACCESS_TOKEN)
        >>> expires_at = response.expires_at
    """
    url = f"{constants.OAUTH_BASE_URL}/introspectToken"
    headers={
      constants.HEADERS.CONTENT_TYPE.value: constants.CONTENT_TYPE.URL_ENCODED.value
    }
    data = {
      'token': access_token,
      'client_id': self.client_id,
      'client_secret': self.client_secret
    }

    request = requests.Request(method=HTTP_METHODS.POST.value, url=url, headers=headers, data=data)
    prepared_request = request.prepare()
    response = self.session.send(prepared_request)
    return IntrospectTokenResponseFormatter.format_response(response)
