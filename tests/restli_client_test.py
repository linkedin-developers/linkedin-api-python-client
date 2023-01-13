from linkedin_api_client.restli_client import RestliClient

def test_restliclient():
  RestliClient.get(resource="/me", access_token="ABC123")