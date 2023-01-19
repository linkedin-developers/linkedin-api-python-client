"""
Example fetching multiple ad campaign groups in a single request using
a BATCH_GET call. This example also illustrates automatic query tunneling.

The 3-legged member access token should include the 'r_ads' or 'rw_ads' scope, which
is part of the Marketing Developer Platform API product.
"""

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from linkedin_api_client.restli_client import RestliClient
import random
from dotenv import load_dotenv,find_dotenv
from requests.exceptions import HTTPError
import curlify

load_dotenv(find_dotenv())

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
AD_CAMPAIGN_GROUPS_RESOURCE = '/adCampaignGroups'
MDP_VERSION = '202212'

restli_client = RestliClient()

ids_list = []
for i in range(0, 400):
  n = random.randint(1000000000,9999999999)
  ids_list.append(n)

try:
  batchResponse = restli_client.batch_get(
    resource_path=AD_CAMPAIGN_GROUPS_RESOURCE,
    ids=ids_list,
    access_token=ACCESS_TOKEN,
    version_string=MDP_VERSION
  )

  # If query tunneling is used, then this will be a POST request with the query param
  # string in the request body
  print("Curl call:")
  print(curlify.to_curl(batchResponse.response.request))

  print("Results:")
  print(batchResponse.statusesMap)
except HTTPError as error:
  print(error)


