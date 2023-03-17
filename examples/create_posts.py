"""
Example calls to create a post on LinkedIn. This requires a member-based token with the following
scopes (r_liteprofile, w_member_social), which is provided by the Sign in with LinkedIn and Share on LinkedIn
API products.

The steps include:
1. Fetching the authenticated member's profile to obtain the member's identifier (a person URN)
2. Create a post using /ugcPosts endpoint (legacy) or /posts endpoint (new)

To view these posts, go to linkedin.com and click Me > Posts & Activity.

BEWARE: This will make an actual post to the main feed which is visible to anyone.
"""

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from linkedin_api.clients.restli.client import RestliClient
import json

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
if ACCESS_TOKEN is None:
    raise Exception(
        'A valid access token must be defined in the /examples/.env file under the variable name "ACCESS_TOKEN"'
    )

ME_RESOURCE = "/me"
UGC_POSTS_RESOURCE = "/ugcPosts"
POSTS_RESOURCE = "/posts"
API_VERSION = "202302"

restli_client = RestliClient()
restli_client.session.hooks["response"].append(lambda r: r.raise_for_status())

"""
Calling the /me endpoint to get the authenticated user's person URN
"""
me_response = restli_client.get(resource_path=ME_RESOURCE, access_token=ACCESS_TOKEN)
print(f"Successfully fetched profile: {json.dumps(me_response.entity)}")


"""
Calling the legacy /ugcPosts API to create a text post on behalf of the authenticated member
"""
ugc_posts_create_response = restli_client.create(
    resource_path=UGC_POSTS_RESOURCE,
    entity={
        "author": f"urn:li:person:{me_response.entity['id']}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "Sample text post created with /ugcPosts API"
                },
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    },
    access_token=ACCESS_TOKEN,
)
print(
    f"Successfully created post using /ugcPosts: {ugc_posts_create_response.entity_id}"
)


"""
Calling the newer, more streamlined (and versioned) /posts API to create a text post on behalf
of the authenticated member
"""
posts_create_response = restli_client.create(
    resource_path=POSTS_RESOURCE,
    entity={
        "author": f"urn:li:person:{me_response.entity['id']}",
        "lifecycleState": "PUBLISHED",
        "visibility": "PUBLIC",
        "commentary": "Sample text post created with /posts API",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
    },
    version_string=API_VERSION,
    access_token=ACCESS_TOKEN,
)
print(f"Successfully created post using /posts: {posts_create_response.entity_id}")
