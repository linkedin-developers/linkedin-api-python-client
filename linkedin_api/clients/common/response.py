from requests import Response
from requests.structures import CaseInsensitiveDict

class BaseResponse:
  def __init__(self, status_code: int, headers: CaseInsensitiveDict[str], url: str, response: Response):
    self.status_code = status_code
    """
    Response status code (e.g. 200, 404, 500, etc.)
    """

    self.response = response
    """
    The raw requests.Response object
    """

    self.headers = headers
    """
    A case-insensitive dictionary of response headers
    """

    self.url = url
    """
    The final URL location of the response
    """