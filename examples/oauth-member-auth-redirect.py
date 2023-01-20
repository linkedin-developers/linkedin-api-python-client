"""
This example illustrates a basic example of the oauth authorization code flow.

Pre-requisites:
. Add CLIENT_ID, CLIENT_SECRET, and OAUTH2_REDIRECT_URL variables to the top-level .env file.
"""
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask,redirect,request
from dotenv import load_dotenv,find_dotenv
from linkedin_api_client.auth.auth_client import AuthClient
from linkedin_api_client.restli_client import RestliClient

load_dotenv(find_dotenv())

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OAUTH2_REDIRECT_URL = os.getenv("OAUTH2_REDIRECT_URL")

app = Flask(__name__)

access_token = None

auth_client = AuthClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=OAUTH2_REDIRECT_URL)
restli_client = RestliClient()

@app.route('/', methods=["GET"])
def main():
  global access_token
  if access_token == None:
    return redirect(auth_client.generate_member_auth_url(scopes=["r_liteprofile","rw_ads"]))
  else:
    return restli_client.get(
      resource="/me",
      access_token=access_token
    )


@app.route('/oauth', methods=["GET"])
def oauth():
  global access_token

  args = request.args
  auth_code = args.get("code")

  if auth_code:
    token_response = auth_client.exchange_auth_code_for_access_token(auth_code)
    access_token = token_response.access_token
    return redirect('/')


if __name__ == '__main__':
    app.run(host='localhost', port=3000)