from typing import Dict, Any

from linkedin_api.clients.common.response import BaseResponse

class BaseAuthResponse(BaseResponse):
  pass

class AccessToken3LResponse(BaseAuthResponse):
  def __init__(self, status_code, url, headers, response, access_token, expires_in, refresh_token, refresh_token_expires_in, scope):
    super().__init__(status_code=status_code, url=url, headers=headers, response=response)
    self.access_token = access_token
    self.expires_in = expires_in
    self.refresh_token = refresh_token
    self.refresh_token_expires_in = refresh_token_expires_in
    self.scope = scope

class AccessToken2LResponse(BaseAuthResponse):
   def __init__(self, status_code, url, headers, response, access_token, expires_in):
    super().__init__(status_code=status_code, url=url, headers=headers, response=response)
    self.access_token = access_token
    self.expires_in = expires_in

class IntrospectTokenResponse(BaseAuthResponse):
    def __init__(self, status_code, url, headers, response, active, auth_type, authorized_at, client_id, created_at, expires_at, scope, status):
      super().__init__(status_code=status_code, url=url, headers=headers, response=response)
      self.active = active
      self.auth_type = auth_type
      self.authorized_at = authorized_at
      self.client_id = client_id
      self.created_at = created_at
      self.expires_at = expires_at
      self.scope = scope
      self.status = status

class RefreshTokenExchangeResponse(BaseAuthResponse):
  def __init__(self, status_code, url, headers, response, access_token, expires_in, refresh_token, refresh_token_expires_in):
    super().__init__(status_code=status_code, url=url, headers=headers, response=response)
    self.access_token = access_token
    self.expires_in = expires_in
    self.refresh_token = refresh_token
    self.refresh_token_expires_in = refresh_token_expires_in
