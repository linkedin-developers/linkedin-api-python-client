
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from linkedin_api.restli_client import RestliClient
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

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