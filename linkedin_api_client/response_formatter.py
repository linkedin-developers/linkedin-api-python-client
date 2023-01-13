from linkedin_api_client.response import EntityResponse, BatchGetResponse
from linkedin_api_client.errors import ResponseFormattingError
from functools import wraps
from requests import Response

def wrap_decode_exception(fn):
  @wraps(fn)
  def wrap(cls, response):
    try:
      return fn(cls, response)
    except Exception as e:
      raise ResponseFormattingError from e
  return wrap

class ResponseFormatter:
  @classmethod
  def format_response(cls, response):
    raise NotImplementedError

class EntityResponseFormatter(ResponseFormatter):
  @classmethod
  @wrap_decode_exception
  def format_response(cls, response) -> EntityResponse:
    return EntityResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      rawData=response.content,
      entity=response.content
    )

class BatchGetResponseFormatter(ResponseFormatter):
  @classmethod
  @wrap_decode_exception
  def format_response(cls, response:Response) -> BatchGetResponse:
    json_data = response.json()
    return BatchGetResponse(
      status_code=response.status_code,
      url=response.url,
      headers=response.headers,
      response=response,
      entitiesMap=json_data["results"],
      statusesMap=json_data["statuses"],
      errorsMap=json_data["errors"]
    )