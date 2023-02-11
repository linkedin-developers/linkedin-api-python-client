"""
Example fetching multiple ad campaign groups in a single request using
a BATCH_GET call. This example also illustrates automatic query tunneling.

The 3-legged member access token should include the 'r_ads' or 'rw_ads' scope, which
is part of the Advertising APIs product.
"""

import os,sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from linkedin_api.clients.restli.client import RestliClient
import random
import curlify

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
AD_CAMPAIGN_GROUPS_RESOURCE = '/adCampaignGroups2'
API_VERSION = '202302'

restli_client = RestliClient()
restli_client.session.hooks['response'].append(lambda r: r.raise_for_status())

# Generate a large, random list of ids
ids_list = []
for i in range(0, 400):
  n = random.randint(1000000000,9999999999)
  ids_list.append(n)

try:
  batchResponse = restli_client.batch_get(
    resource_path=AD_CAMPAIGN_GROUPS_RESOURCE,
    ids=ids_list,
    access_token=ACCESS_TOKEN,
    version_string=API_VERSION
  )

  # If query tunneling is used, then this will be a POST request with the query param
  # string in the request body
  print("Curl call:")
  print(f"{curlify.to_curl(batchResponse.response.request)}\n")

  print("Results:")
  print(batchResponse.statuses)
except Exception as error:
  print(f"Error: {error}")

