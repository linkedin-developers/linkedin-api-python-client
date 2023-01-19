from linkedin_api_client.request_builder import RequestBuilder
from linkedin_api_client.restli_client import RestliClient
from typing import Generic, Type, TypeVar

T = TypeVar('T')
V = TypeVar('V')

class Request2(Generic[T]):


restli_request = (
    RequestBuilder
        .finder(
          resource_path="/adAccounts",
          finder_name="search",
          access_token="ACCESS_TOKEN"
        )
        .set_start(2)
        .set_count(5)
        .build()
)

restli_client = RestliClient()

response = restli_client.request2()


class CollectionResponse:
  def doCollectionStuff(self):
    pass

class RequestClass(Generic[T]):
  pass

class Client:
  def request(self, requestObj: RequestClass[V]) -> V:
    return {}

request_object = RequestClass[CollectionResponse]()
client = Client()
response = client.request(request_object)
response.doCollectionStuff()


finder_response = restli_client.request(restli_request)
finder_response.elements

finderRequest = FinderRequestBuilder(
    resource_path=AD_ACCOUNTS_RESOURCE,
    access_token=ACCESS_TOKEN
).set_start(2).set_count(10).build()

restli_client.finder2(finderRequest)

request = RestliRequest[CollectionResponse]()
response = restli_client.request(restli_request=request)

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar('T')      # Declare type variable

def first(l: Sequence[T]) -> T:   # Generic function
    return l[0]

input = Sequence[CollectionResponse]()
first(input)