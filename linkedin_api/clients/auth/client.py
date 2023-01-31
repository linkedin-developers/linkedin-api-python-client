import requests
from linkedin_api.clients.auth.response_formatter import AccessToken3LResponseFormatter
import linkedin_api.common.constants as constants
from linkedin_api.common.errors import MissingArgumentError
import linkedin_api.clients.auth.utils.oauth as oauth
from linkedin_api.clients.auth.response import AccessToken3LResponse
from typing import Optional, List
from linkedin_api.common.constants import HTTP_METHODS

class AuthClient:
  def __init__(self, client_id: str, client_secret: str, redirect_url: Optional[str] = None):
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_url = redirect_url
    self.session = requests.Session()


  def generate_member_auth_url(self, scopes: List[str], state: Optional[str] = None) -> str:
    if self.redirect_url is None:
      raise MissingArgumentError("The redirect_url is missing from the AuthClient.")

    return oauth.generate_member_auth_url(
      client_id = self.client_id,
      redirect_url = self.redirect_url,
      scopes = scopes,
      state = state
    )

  def exchange_auth_code_for_access_token(self, code: str):
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

  def exchange_refresh_token_for_access_token(self, refresh_token: str):
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
    return self.session.send(prepared_request)

  def get_two_legged_access_token(self):
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
    return self.session.send(prepared_request)

  def introspect_access_token(self, access_token: str):
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
    return self.session.send(prepared_request)
