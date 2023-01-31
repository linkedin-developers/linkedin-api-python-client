from abc import ABC, abstractmethod
from functools import wraps
from typing import Generic, TypeVar
from requests import Response
from linkedin_api.common.errors import ResponseFormattingError
from linkedin_api.clients.common.response import BaseResponse


def wrap_format_exception(fn):
  @wraps(fn)
  def wrap(cls, response: Response):
    try:
      return fn(cls, response)
    except Exception as e:
      raise ResponseFormattingError from e
  return wrap

T = TypeVar('T', bound=BaseResponse)

class BaseResponseFormatter(ABC, Generic[T]):
  @classmethod
  @abstractmethod
  def format_response(cls, response: Response) -> T:
    pass