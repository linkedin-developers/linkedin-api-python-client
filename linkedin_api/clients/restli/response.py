from typing import Dict, Optional, Any, Union, List, TypedDict
from requests import Response
from requests.structures import CaseInsensitiveDict
from linkedin_api.clients.common.response import BaseResponse
from linkedin_api.clients.restli.types import RestliEntity, EncodedEntityId


class Paging:
  def __init__(self, start: Optional[int] = None, count: Optional[int] = None, total: Optional[int] = None):
    self.start = start
    """
    The start index of returned results (zero-based index).
    """

    self.count = count
    """
    The number of results returned in the response.
    """

    self.total = total
    """
    The total number of results available.
    """

class BaseRestliResponse(BaseResponse):
  pass


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
    self.entity = entity
    """
    The representation (typically a dictionary) of the retrieved entity, decoded from the json-encoded response content.
    """


class BatchGetResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    results: Dict[EncodedEntityId, RestliEntity],
    statuses: Dict[EncodedEntityId, int],
    errors: Dict[EncodedEntityId, Any]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.results = results
    """
    A map of entities that were successfully retrieved, with the key being the encoded entity id, and the value being a dictionary representing the entity.
    """

    self.statuses = statuses
    """
    A map of entities and status code, with the key being the encoded entity id, and the value being the status code number value.
    """

    self.errors = errors
    """
    A map containing entities that could not be successfully fetched, with the key being the encoded entity id, and the value being the error response.
    """

class CollectionResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    elements: List[RestliEntity],
    paging: Paging,
    metadata: Optional[Any]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.elements = elements
    """
    The list of entities returned in the response.
    """

    self.paging = paging
    """
    Paging metadata object
    """

    self.metadata = metadata
    """
    Optional response metadata object
    """

class BatchFinderResult:
  def __init__(self, elements: List[RestliEntity], paging: Optional[Paging] = None, metadata = None, error = None, isError: bool = False):
    self.elements = elements
    """
    The list of entities found for the corresponding finder criteria.
    """

    self.paging = paging
    """
    Optional paging metadata object
    """

    self.metadata = metadata
    """
    Optional response metadata object
    """

    self.error = error
    """
    Optional error details if finder call failed
    """

    self.isError = isError
    """
    Flag if this finder call experienced an error
    """

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
    """
    The list of finder results, in the same order as the requested batch finder search criteria list.
    """

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
    """
    The encoded entity id of the created entity
    """

    self.entity = entity
    """
    Optional created entity. Some APIs support returning the created entity to eliminate the need for a subsequent GET call.
    """

class BatchCreateResult:
  def __init__(self, status: int, id: str, error: Any):
    self.status = status
    """
    The status code of the individual create call.
    """

    self.id = id
    """
    The id of the created entity.
    """

    self.error = error
    """
    Error details if the create call experienced an error.
    """

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
    """
    The list of batch create results, corresponding to the order of the `entities` request parameter
    """

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
    """
    Optional entity after the update. Some APIs support returning the updated entity to eliminate the need for a subsequent GET call.
    """


class BatchUpdateResult():
  # TODO add support for return entity
  def __init__(self, status: int):
    self.status = status
    """
    The status code of the individual update call
    """

class BatchUpdateResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    results: Optional[Dict[EncodedEntityId, BatchUpdateResult]]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.results = results
    """
    The results map where the keys are the encoded entity ids, and the values are the individual update call results, which includes the status code.
    """

class BatchDeleteResult():
  def __init__(self, status: int):
    self.status = status
    """
    The status code of the delete call.
    """

class BatchDeleteResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    results: Optional[Dict[EncodedEntityId, BatchDeleteResult]]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.results = results
    """
    The results map where the keys are the encoded entity ids, and the values are the individual delete call results, which includes the status code.
    """

class ActionResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: CaseInsensitiveDict[str],
    response: Response,
    value: Optional[Any]
  ):
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self.value = value
    """
    The action response value.
    """

