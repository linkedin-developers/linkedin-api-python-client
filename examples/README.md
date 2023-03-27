## LinkedIn API Python Client Examples

This directory contains examples showing how to use the LinkedIn API Python client library.

### Steps to Run

1. Activate virtual environment: `poetry shell`
2. Navigate inside the `/examples` directory
3. Create a `.env` file that contains the following variables that will be used when running the examples. Only some of these variables may actually be needed to run a particular script. Check the specific example comments on more specific requirements (e.g. required scopes for the access token).
  ```sh
  ACCESS_TOKEN="your_valid_access_token"
  CLIENT_ID="your_app_client_id"
  CLIENT_SECRET="your_app_client_secret"
  OAUTH2_REDIRECT_URL="your_app_oauth2_redirect_url"
  ```
4. Execute the desired example script: `python3 {script filename}`. For example: `python3 get_profile.py`

### Example Notes

| Example filename | Description |
|---|---|
| `oauth_member_auth_redirect.py` | Demonstrates the member oauth redirect flow (authorization code flow) to obtain a 3-legged access token. |
| `oauth_2legged.py` | Obtains a 2-legged access token and performs introspection. |
| `get_profile.py` | Uses Sign In With LinkedIn v1 to fetch member profile. Also demonstrates use of field projections and decoration. |
| `create_posts.py` | Uses Sign In With LinkedIn v1 and Share on LinkedIn to create posts. |
| `crud_ad_accounts.py` | Performs create, get, finder, partial update, and delete requests on ad accounts. |
| `batch_get_campaign_groups_query_tunneling.py` | Demonstrates a request that requires query tunneling, which is performed automatically by the client. |
