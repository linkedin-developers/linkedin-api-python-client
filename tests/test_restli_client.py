from linkedin_api_client import restli_client

def test_addNums():
  assert restli_client.addNums(2,3) == 5