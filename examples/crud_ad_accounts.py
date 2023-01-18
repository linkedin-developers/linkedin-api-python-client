
# Sets the path to locate local linkedin_api_client module
from dotenv import load_dotenv, find_dotenv
from linkedin_api_client.request_builder import FinderRequestBuilder, RequestBuilder
from linkedin_api_client.restli_client import RestliClient
from linkedin_api_client.response import CollectionResponse
from linkedin_api_client.request import RestliRequest
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Load the app credentials info from the examples/.env file
load_dotenv(find_dotenv())
from typing import Type

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
AD_ACCOUNTS_RESOURCE = '/adAccounts'
MDP_VERSION = '202212'

restli_client = RestliClient()

'''
Find ad accounts by search criteria
'''
r = restli_client.finder(
    resource_path_template=AD_ACCOUNTS_RESOURCE,
    finder_name='search',
    query_params={
        "search": {
            "status": {
                "values": ["ACTIVE", "DRAFT", "CANCELED"]
            },
            "test": False
        },
        "start": 0,
        "count": 5
    },
    access_token=ACCESS_TOKEN,
    version_string=MDP_VERSION
)
print("Find ad accounts result: ", json.dumps(r.elements))
print(f"Total results: {r.paging.total}")

request = (
  RequestBuilder.finder(
    resource_path_template=AD_ACCOUNTS_RESOURCE,
    finder_name="search",
    access_token=ACCESS_TOKEN
  )
    .set_query_params({
      "search": {
          "status": {
              "values": ["ACTIVE", "DRAFT", "CANCELED"]
          },
          "test": False
      }
    })
    .set_start(1)
    .set_count(5)
    .build()
)

response = restli_client.request(request)