import requests
import linkedin_api_client.constants as constants
import linkedin_api_client.utils.oauth as oauth

class AuthClient:
  def __init__(self, client_id, client_secret, redirect_url):
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_url = redirect_url

  def get_two_legged_access_token(self):
    url = f"{constants.OAUTH_BASE_URL}/accessToken"

    data = {
      'grant_type': 'client_credentials',
      'client_id': self.client_id,
      'client_secret': self.client_secret
    }

    requests.post(url, data, headers={
      constants.HEADERS.CONTENT_TYPE: constants.CONTENT_TYPE.URL_ENCODED
    })

  def generate_member_auth_url(self, scopes: list, state: str = None) -> str:
    return oauth.gnerate_member_auth_url(
      client_id = self.client_id,
      redirect_url = self.redirect_url,
      scopes = scopes,
      state = state
    )

  def exchange_auth_code_for_access_token(self, code: str):
    url = f"{constants.OAUTH_BASE_URL}/accessToken"
    data = {
      "grant_type": "authorization_code",
      "code": code,
      "client_id": self.client_id,
      "client_secret": self.client_secret,
      "redirect_uri": self.redirect_url
    }
    headers = {
      constants.HEADERS.CONTENT_TYPE: constants.CONTENT_TYPE.URL_ENCODED
    }

    return requests.post(url, data=data, headers=headers)

