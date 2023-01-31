"""
Example call to fetch the member profile for the authorized member.

The 3-legged member access token should include the 'r_liteprofile' scope, which
is part of the Sign In With LinkedIn API product.
"""

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from linkedin_api.clients.restli.client import RestliClient

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
if ACCESS_TOKEN is None:
  raise Exception('A valid access token must be defined in the /examples/.env file under the variable name "ACCESS_TOKEN"')

PROFILE_RESOURCE = "/me"

restli_client = RestliClient()

"""
Basic usage to fetch current member profile
"""
response = restli_client.get(
  resource_path=PROFILE_RESOURCE,
  access_token=ACCESS_TOKEN
)
print("Basic usage:", response.entity)

"""
Usage with field projections
"""
response = restli_client.get(
  resource_path=PROFILE_RESOURCE,
  access_token=ACCESS_TOKEN,
  query_params={
    "fields": "id,firstName:(localized),lastName"
  }
)
print("\n\nUsage with field projections:", response.entity)

"""
Usage with decoration of displayImage
"""
response = restli_client.get(
  resource_path=PROFILE_RESOURCE,
  access_token=ACCESS_TOKEN,
  query_params={
    "projection": "(id,firstName,lastName,profilePicture(displayImage~:playableStreams))"
  }
)
print("\n\nUsage with decoration:", response.entity)

