from requests import PreparedRequest
from constants import RESTLI_METHODS
from typing import Dict, Any
from linkedin_api_client.utils.query_tunneling import maybe_apply_query_tunneling_get_requests
import linkedin_api_client.utils.api as apiutils
import linkedin_api_client.utils.encoder as encoder
from linkedin_api_client.utils.restli import encode_query_params_for_get_requests
from linkedin_api_client.response_formatter import CollectionResponseFormatter
from linkedin_api_client.request import RestliRequest
from linkedin_api_client.response import CollectionResponse
from linkedin_api_client.constants import HTTP_METHODS

import copy

class RestliRequestBuilder:
  def __init__(self, restli_method:str, resource_path: str, access_token: str):
    self.restli_method = restli_method
    self.resource_path = resource_path
    self.access_token = access_token

  def set_query_params(self, query_params: Dict[str, Any]):
    self.query_params = query_params
    return self

  def set_path_keys(self, path_keys: Dict[str, Any]):
    self.path_keys = path_keys
    return self

  def set_version_string(self, version_string: str = None):
    self.version_string = version_string
    return self

  def _build_base_url(self):
    return apiutils.build_rest_url(
      resource_path=self.resource_path,
      path_keys=getattr(self, "path_keys"),
      version_string=getattr(self, "version_string")
    )

  def _build_final_query_params(self):
    return copy.deepcopy(getattr(self, "query_params", {}))

  def _build_final_encoded_query_param_string(self):
    final_query_params = self._build_final_query_params()
    return encoder.param_encode(final_query_params)

  def build() -> RestliRequest:
    raise NotImplementedError


class BaseGetRequestBuilder(RestliRequestBuilder):
  def set_fields(self, fields: str):
    self.fields = fields
    return self

  def set_decoration(self, decoration: str):
    self.decoration = decoration
    return self

  def _build_final_query_params(self):
    query_params_final = copy.deepcopy(getattr(self, "query_params", {}))

    fields = getattr(self, "fields", None)
    if fields is not None:
      query_params_final.update({ "fields": fields })

    decoration = getattr(self, "decoration", None)
    if decoration is not None:
      query_params_final.update({ "projection": decoration })

    return query_params_final

  def _build_final_encoded_query_param_string(self):
    final_query_params = self._build_final_query_params
    return encode_query_params_for_get_requests(final_query_params)


class FinderRequestBuilder(BaseGetRequestBuilder):
  def __init__(self, resource_path: str, access_token: str, finder_name: str):
    super().__init__(restli_method=RESTLI_METHODS.FINDER.value, resource_path=resource_path, access_token=access_token)
    self.finder_name = finder_name
    self.response_formatter = CollectionResponseFormatter

  def set_start(self, start: int):
    self.start = start
    return self

  def set_count(self, count: int):
    self.count = count
    return self

  def _build_final_query_params(self):
    query_params_final = super()._build_final_query_params()

    start = getattr(self, "start", None)
    if start is not None:
      query_params_final.update({ "start": start })

    count = getattr(self, "count", None)
    if count is not None:
      query_params_final.update({ "count": count })

    return query_params_final

  def build(self) -> RestliRequest[CollectionResponse]:
    final_request = maybe_apply_query_tunneling_get_requests(
      encoded_query_param_string=self._build_final_encoded_query_param_string(),
      url=self._build_base_url(),
      original_restli_method=self.restli_method,
      access_token=self.access_token,
      version_string=getattr(self, "version_string")
    )

    return RestliRequest[CollectionResponse](
      method=final_request.method,
      url=final_request.url,
      headers=final_request.headers,
      data=final_request.data,
      response_formatter=self.response_formatter
    )




class RequestBuilder:
  @classmethod
  def finder(cls, resource_path: str, finder_name: str, access_token: str) -> FinderRequestBuilder:
    return FinderRequestBuilder(
      resource_path=resource_path,
      access_token=access_token,
      finder_name=finder_name
    )










