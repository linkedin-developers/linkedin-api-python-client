from linkedin_api_client.restli_client import RestliClient
import os

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

print(RestliClient.get(resource="/me", access_token=ACCESS_TOKEN))