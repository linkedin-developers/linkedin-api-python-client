"""
Example calls to perform CRUD and finder operations on ad accounts using versioned APIs.
This will create a test ad account, fetch it directly, find it using search criteria, update it, and delete it.

The 3-legged member access token should include the 'rw_ads' scope, which is part of the
Advertising APIs product.
"""

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from linkedin_api.clients.restli.client import RestliClient
import json

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
if ACCESS_TOKEN is None:
  raise Exception('A valid access token must be defined in the /examples/.env file under the variable name "ACCESS_TOKEN"')

AD_ACCOUNTS_RESOURCE = '/adAccounts'
AD_ACCOUNTS_ENTITY_RESOURCE = '/adAccounts/{id}'
API_VERSION = '202212'

restli_client = RestliClient()
restli_client.session.hooks['response'].append(lambda r: r.raise_for_status())


"""
Create a test ad account
"""
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
    version_string=API_VERSION
  )
ad_account_id = create_response.entity_id
print(f"Successfully created ad account: {ad_account_id}\n")


"""
Get the created ad account
"""
get_response = restli_client.get(
  resource_path=AD_ACCOUNTS_ENTITY_RESOURCE,
  path_keys={
    "id": ad_account_id
  },
  access_token=ACCESS_TOKEN,
  version_string=API_VERSION
)
print(f"Successfully fetched ad account: {json.dumps(get_response.entity)}\n")


"""
Partial update on ad account
"""
partial_update_response = restli_client.partial_update(
  resource_path=AD_ACCOUNTS_ENTITY_RESOURCE,
  path_keys={
    "id": ad_account_id
  },
  patch_set_object={
    "name": "Modified Test Ad Account"
  },
  access_token=ACCESS_TOKEN,
  version_string=API_VERSION
)
print(f"Successfully updated ad account\n")


"""
Find ad accounts by search criteria
"""
r = restli_client.finder(
    resource_path=AD_ACCOUNTS_RESOURCE,
    finder_name="search",
    query_params={
        "search": {
            "reference": {
              "values": ["urn:li:organization:123"]
            },
            "name": {
              "values": ["Modified Test Ad Account"]
            },
            "test": True
        },
        "start": 0,
        "count": 5
    },
    access_token=ACCESS_TOKEN,
    version_string=API_VERSION
)
print("Find ad accounts result: ", json.dumps(r.elements))
print(f"Total results: {r.paging.total}\n")


"""
Delete ad account
"""
delete_response = restli_client.delete(
  resource_path=AD_ACCOUNTS_ENTITY_RESOURCE,
  path_keys={
    "id": ad_account_id
  },
  access_token=ACCESS_TOKEN,
  version_string=API_VERSION
)
print("Successfully deleted ad account\n")