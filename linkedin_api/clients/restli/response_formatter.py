from linkedin_api.clients.common.response_formatter import BaseResponseFormatter, wrap_format_exception
from linkedin_api.clients.restli.response import *
from linkedin_api.clients.restli.utils.restli import get_created_entity_id
from requests import Response

class GetResponseFormatter(BaseResponseFormatter[GetResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response) -> GetResponse:
    json_data = response.json()

    return GetResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      entity=json_data
    )


class BatchGetResponseFormatter(BaseResponseFormatter[BatchGetResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response:Response) -> BatchGetResponse:
    json_data = response.json()
    return BatchGetResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      resultsMap=getattr(json_data, "results", None),
      statusesMap=getattr(json_data, "statuses", None),
      errorsMap=getattr(json_data, "errors", None)
    )

class CollectionResponseFormatter(BaseResponseFormatter[CollectionResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> CollectionResponse:
    json_data = response.json()
    paging = getattr(json_data, "paging", None)

    return CollectionResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      elements=getattr(json_data, "elements", None),
      paging=Paging(
        getattr(paging, "start", None),
        getattr(paging, "count", None),
        getattr(paging, "total", None)
      ),
      metadata=getattr(json_data, "metadata", None)
    )

class BatchFinderResponseFormatter(BaseResponseFormatter[BatchFinderResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> BatchFinderResponse:
    json_data = response.json()
    elements = getattr(json_data, "elements", None)
    finder_results = [ cls.format_finder_result(result) for result in elements ] if elements else None

    return BatchFinderResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      results=finder_results
    )

  @classmethod
  @wrap_format_exception
  def format_finder_result(cls, result) -> BatchFinderResult:
    return BatchFinderResult(
      getattr(result, "elements", None),
      getattr(result, "paging", None),
      getattr(result, "metadata", None),
      getattr(result, "error", None),
      getattr(result, "isError", None)
    )

class CreateResponseFormatter(BaseResponseFormatter[CreateResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> CreateResponse:
    json_data = response.json()

    return CreateResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      entityId=get_created_entity_id(response, True),
      entity=json_data if json_data else None
    )

class BatchCreateResponseFormatter(BaseResponseFormatter[BatchCreateResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> BatchCreateResponse:
    json_data = response.json()
    elements = getattr(json_data, "elements", None)
    batch_create_results = [ cls.format_batch_create_result(result) for result in elements ]

    return BatchCreateResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      elements=batch_create_results
    )

  @classmethod
  @wrap_format_exception
  def format_batch_create_result(cls, result) -> BatchCreateResult:
    return BatchCreateResult(
      getattr(result, "status", None),
      getattr(result, "id", None),
      getattr(result, "error", None)
    )

class UpdateResponseFormatter(BaseResponseFormatter[UpdateResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> UpdateResponse:
    json_data = response.json()

    return UpdateResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      entity=json_data if json_data is not None else None
    )

class BatchUpdateResponseFormatter(BaseResponseFormatter[BatchUpdateResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> BatchUpdateResponse:
    json_data = response.json()
    results = getattr(json_data, "results", None)
    if results is not None:
      batch_update_results = { encoded_id:cls.format_batch_update_result(result) for (encoded_id, result) in results.items() }

    return BatchUpdateResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      results=batch_update_results
    )

  @classmethod
  @wrap_format_exception
  def format_batch_update_result(cls, result) -> BatchUpdateResult:
    return BatchUpdateResult(
      status=getattr(result, "status")
    )

class DeleteResponseFormatter(BaseResponseFormatter[BaseRestliResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> BaseRestliResponse:
    return BaseRestliResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response
    )

class BatchDeleteResponseFormatter(BaseResponseFormatter[BatchDeleteResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> BatchDeleteResponse:
    json_data = response.json()
    results = getattr(json_data, "results", None)
    if results is not None:
      batch_delete_results = { encoded_id:cls.format_batch_delete_result(result) for (encoded_id, result) in results.items() }

    return BatchDeleteResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      results=batch_delete_results
    )

  @classmethod
  @wrap_format_exception
  def format_batch_delete_result(cls, result) -> BatchDeleteResult:
    return BatchDeleteResult(
      status=getattr(result, "status")
    )

class ActionResponseFormatter(BaseResponseFormatter[ActionResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> ActionResponse:
    json_data = response.json()

    return ActionResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      value=getattr(json_data, "value", None)
    )