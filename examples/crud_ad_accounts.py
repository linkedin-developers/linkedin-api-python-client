
# Sets the path to locate local linkedin_api_client module
from dotenv import load_dotenv, find_dotenv
from linkedin_api.restli_client.client import RestliClient
from linkedin_api.restli_client.response import CollectionResponse
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Load the app credentials info from the examples/.env file
load_dotenv(find_dotenv())
from typing import Type

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
if ACCESS_TOKEN is None:
  raise Exception('A valid access token must be defined in the /examples/.env file under the variable name "ACCESS_TOKEN"')

AD_ACCOUNTS_RESOURCE = '/adAccounts'
MDP_VERSION = '202212'

restli_client = RestliClient()

create_response = restli_client.create(
    resource_path=AD_ACCOUNTS_RESOURCE,
    entity={
      "name": 'Test Ad Account',
      "reference": 'urn:li:organization:123',
      "status": 'DRAFT',
      "type": 'BUSINESS',
      "test": True
    },
    access_token=ACCESS_TOKEN,
    version_string=MDP_VERSION
  )
print(f"Successfully created ad account: {create_response.entity_id}")

restli_client.delete(
  resource_path=f"{AD_ACCOUNTS_RESOURCE}/{id}",
  path_keys={
    "id": create_response.entity_id
  },
  access_token=ACCESS_TOKEN,
  version_string=MDP_VERSION
)
print(f"Successfully deleted ad account.")


'''
Find ad accounts by search criteria
'''
r = restli_client.finder(
    resource_path=AD_ACCOUNTS_RESOURCE,
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



response = restli_client.request(request)