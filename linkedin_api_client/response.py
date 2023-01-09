from typing import Dict, Optional, Any

class Response:
  """

  """
  def __init__(self, status: int, headers: dict, body: Optional[Dict[str, Any]] = None):
    self.status = status
    self.body = body
    self.headers = headers

class EntityResponse(Response):
  @property
  def entity(self):
    return self.body


class CollectionResponse(Response):
  @property
  def elements(self):
    return self.body.elements

  @property
  def paging(self):
    return self.body.paging

  @property
  def metadata(self):
    return self.body.metadata


