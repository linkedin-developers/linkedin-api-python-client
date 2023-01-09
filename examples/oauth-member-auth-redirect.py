from flask import Flask,redirect,request
import os
from linkedin_api_client.auth_client import AuthClient
from linkedin_api_client.restli_client import RestliClient

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OAUTH2_REDIRECT_URL = os.getenv("OAUTH2_REDIRECT_URL")

app = Flask(__name__)

access_token = None

auth_client = AuthClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=OAUTH2_REDIRECT_URL)
restli_client = RestliClient()

@app.route('/', methods=["GET"])
def main():
  if access_token == None:
    redirect(auth_client.generate_member_auth_url(scopes=["r_liteprofile","r_organization","rw_ads"]))
  else:
    return restli_client.get(
      resource="/me",
      access_token=access_token
    )


@app.route('/oauth', methods=["GET"])
def oauth():
  args = request.args
  auth_code = args.get("code")

  if auth_code:
    token_response = auth_client.exchange_auth_code_for_access_token(auth_code)
    access_token = token_response.access_token
    redirect('/')

if __name__ == '__main__':
    app.run(host='localhost', port=3000)