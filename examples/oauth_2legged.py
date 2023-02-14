"""
Example calls to fetch a 2-legged access token and introspect the token. A 2-legged access token
obtained using the Client Credentials Flow, allows your application to access APIs that are not member
specific.

Note: By default, developer applications do NOT have the Client Credentials Flow (2-legged) enabled. This
example will only work if your application has had this flow enabled.
"""

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from linkedin_api.clients.auth.client import AuthClient

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

auth_client = AuthClient(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET
)

token_response = auth_client.get_two_legged_access_token()
access_token = token_response.access_token
print(f"Status code: {token_response.status_code}")
print(f"Access token: {access_token}\n")

if access_token:
  introspection_response = auth_client.introspect_access_token(access_token)
  print("Token introspection details:")
  print(f"Auth type: {introspection_response.auth_type}")
  print(f"Expires at: {introspection_response.expires_at}")