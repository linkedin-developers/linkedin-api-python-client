from typing import Dict, Optional, Any, Union
from requests import Response

EncodedEntityId = str
"""
Represents an encoded entity id
"""

RestliEntity = Dict[str, Any]
"""
Represents a Rest.li entity record
"""

class BaseRestliResponse:
  """

  """
  def __init__(self, status_code: int, headers: dict, url: str, response: Response = None):
    self.status_code = status_code
    self.response = response
    self.headers = headers
    self.url = url

class EntityResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: Dict[str, str],
    rawData,
    entity: Union[Dict[str, Any], str, int, bool]
  ) -> None:
    super().__init__(status_code, headers, url, rawData)
    self._entity = entity

  @property
  def entity(self):
    return self._entity


class BatchGetResponse(BaseRestliResponse):
  def __init__(
    self,
    status_code: int,
    url: str,
    headers: Dict[str, str],
    response: Response,
    entitiesMap: Dict[EncodedEntityId, RestliEntity],
    statusesMap: Dict[EncodedEntityId, int],
    errorsMap: Dict[EncodedEntityId, Any]
  ) -> None:
    super().__init__(status_code=status_code, headers=headers, url=url, response=response)
    self._entitiesMap = entitiesMap
    self._statusesMap = statusesMap
    self._errorsMap = errorsMap

  @property
  def entitiesMap(self) -> Dict[EncodedEntityId, RestliEntity]:
    """
    Returns:
        Dict[EncodedEntityId, RestliEntity]: A map of entities that were successfully retrieved.
    """
    return self._entitiesMap

  @property
  def statusesMap(self) -> Dict[EncodedEntityId, int]:
    """
    Returns:
        Dict[EncodedEntityId, int]: A map of entities and their corresponding status code
    """
    return self._statusesMap

  @property
  def errorsMap(self) -> Dict[EncodedEntityId, Any]:
    """
    Returns:
        Dict[EncodedEntityId, Any]: A map containing entities that could not be successfully fetched
        and their associated error responses
    """
    return self._errorsMap