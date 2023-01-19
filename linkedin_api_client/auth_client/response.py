from typing import Dict, Any

class AccessToken3LResponse:
  def __init__(self, data: Dict[str, Any]):
    self._data = data

  @property
  def access_token(self) -> str:
    """
    The 3-legged access token
    """
    return self._data["access_token"]

  @property
  def expires_in(self) -> int:
    return self._data["expires_in"]

  @property
  def refresh_token(self):
    return self._data["refresh_token"]

  @property
  def refresh_token_expires_in(self):
    return self._data["refresh_token_expires_in"]

  @property
  def scope(self):
    return self._data["scope"]
