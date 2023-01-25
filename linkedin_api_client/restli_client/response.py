from typing import Dict, Optional, Any, Union, List, TypedDict
from requests import Response
from requests.structures import CaseInsensitiveDict
from linkedin_api_client.restli_client.types import RestliEntity, EncodedEntityId


class Paging:
  def __init__(self, start: int, count: int, total: int):
    self.start = start
    self.count = count
    self.total = total


class BaseRestliResponse:
  def __init__(self, status_code: int, headers: CaseInsensitiveDict[str], url: str, response: Response):
    self.status_code = status_code
    self.response = response
    self.headers = headers
    self.url = url

class GetResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    entity: Union[Dict[str, Any], str, int, bool]
  ) -> None:
    super().__init__(status_code, headers, url, response)
    self._entity = entity

  @property
  def entity(self):
    return self._entity


class BatchGetResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    resultsMap: Dict[EncodedEntityId, RestliEntity],
    statusesMap: Dict[EncodedEntityId, int],
    errorsMap: Dict[EncodedEntityId, Any]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.resultsMap = resultsMap
    self.statusesMap = statusesMap
    self.errorsMap = errorsMap

class CollectionResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    elements: List[RestliEntity],
    paging: Optional[Paging],
    metadata: Optional[Any]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.elements = elements
    self.paging = paging
    self.metadata = metadata

class BatchFinderResult:
  def __init__(self, elements: List[RestliEntity], paging: Optional[Paging] = None, metadata = None, error = None, isError: bool = False):
    self.elements = elements
    self.paging = paging
    self.metadata = metadata
    self.error = error
    self.isError = isError

class BatchFinderResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    results: List[BatchFinderResult]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.results = results

class CreateResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    entity_id: Optional[EncodedEntityId] = None,
    entity: Optional[RestliEntity] = None
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.entity_id = entity_id
    self.entity = entity

class BatchCreateResult:
  def __init__(self, status: int, id: str, error: Any):
    self.status = status
    self.id = id
    self.error = error

class BatchCreateResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    elements: List[BatchCreateResult]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.elements = elements

class UpdateResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    entity: Optional[RestliEntity]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.entity = entity

class BatchUpdateResult(TypedDict):
  # TODO add support for return entity
  status: int

class BatchUpdateResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    results: Dict[EncodedEntityId, BatchUpdateResult]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.results = results

class BatchDeleteResult(TypedDict):
  status: int

class BatchDeleteResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    results: Dict[EncodedEntityId, BatchDeleteResult]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.results = results

class ActionResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    value: Any
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.value = value

