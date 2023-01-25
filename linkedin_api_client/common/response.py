from requests import Response
from requests.structures import CaseInsensitiveDict

class BaseResponse:
  def __init__(self, status_code: int, headers: CaseInsensitiveDict[str], url: str, response: Response):
    self.status_code = status_code
    self.response = response
    self.headers = headers
    self.url = url