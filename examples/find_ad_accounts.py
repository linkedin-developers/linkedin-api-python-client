from linkedin_api_client.restli_client import RestliClient
import os

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

r = RestliClient.finder(
  resource='/adAccountsV2',
  finder_name='search',
  query_params={
    "search": {
      "status": {
        "values": ["ACTIVE", "DRAFT", "CANCELED"]
      },
      "type": {
        "values": ["BUSINESS", "ENTERPRISE"]
      },
      "test": True
    }
  },
  access_token=ACCESS_TOKEN
)

print("Results:")
print(r)