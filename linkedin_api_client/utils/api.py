import linkedin_api_client.constants as constants

def getRestApiBaseUrl(version_string):
  if version_string:
    return constants.VERSIONED_BASE_URL
  else:
    return constants.NON_VERSIONED_BASE_URL

def getRestliRequestHeaders(*, restli_method, access_token, version_string=None, http_method_override=None, content_type="application/json"):
  headers = {
    "Connection": "Keep-Alive",
    "X-RestLi-Protocol-Version": "2.0.0",
    "X-RestLi-Method": restli_method,
    "Authorization": "Bearer " + access_token,
    "Content-Type": content_type
  }
  if (version_string is not None):
    headers.update({ "LinkedIn-Version": version_string })
  if (http_method_override is not None):
    headers.update({ "X-HTTP-Method-Override": http_method_override })

  return headers

