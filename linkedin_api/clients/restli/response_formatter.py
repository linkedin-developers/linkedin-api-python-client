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
      results=json_data.get("results", None),
      statuses=json_data.get("statuses", None),
      errors=json_data.get("errors", None)
    )

class CollectionResponseFormatter(BaseResponseFormatter[CollectionResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> CollectionResponse:
    json_data = response.json()
    paging = json_data.get("paging", None)

    return CollectionResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      elements=json_data.get("elements", None),
      paging=Paging(
        paging.get("start", None),
        paging.get("count", None),
        paging.get("total", None)
      ) if paging else Paging(),
      metadata=getattr(json_data, "metadata", None)
    )

class BatchFinderResponseFormatter(BaseResponseFormatter[BatchFinderResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> BatchFinderResponse:
    json_data = response.json()
    elements = json_data.get("elements", None)
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
  def format_finder_result(cls, result: Dict) -> BatchFinderResult:
    return BatchFinderResult(
      result.get("elements", None),
      result.get("paging", None),
      result.get("metadata", None),
      result.get("error", None),
      result.get("isError", False)
    )

class CreateResponseFormatter(BaseResponseFormatter[CreateResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> CreateResponse:
    try:
      json_data = response.json()
    except ValueError:
      # Handle case of no entity returned in the response
      json_data = None

    return CreateResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      entity_id=get_created_entity_id(response, True),
      entity=json_data if json_data else None
    )

class BatchCreateResponseFormatter(BaseResponseFormatter[BatchCreateResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> BatchCreateResponse:
    json_data = response.json()
    elements = json_data.get("elements", None)
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
      result.get("status", None),
      result.get("id", None),
      result.get("error", None)
    )

class UpdateResponseFormatter(BaseResponseFormatter[UpdateResponse]):
  @classmethod
  @wrap_format_exception
  def format_response(cls, response: Response) -> UpdateResponse:
    try:
      json_data = response.json()
    except ValueError:
      json_data = None

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
    results = json_data.get("results", None)
    if results is not None:
      batch_update_results = { encoded_id:cls.format_batch_update_result(result) for (encoded_id, result) in results.items() }
    else:
      batch_update_results = None

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
      status=result.get("status", None)
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
    results = json_data.get("results", None)
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
      status=result.get("status", None)
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
      value=json_data.get("value", None)
    )