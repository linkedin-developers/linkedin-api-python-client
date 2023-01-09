import requests
import copy
from typing import Union
import linkedin_api_client.utils.api as apiutils
import linkedin_api_client.utils.encoder as encoder
from linkedin_api_client.constants import RESTLI_METHODS

class RestliClient:
  def get(*, resource, id: Union[str, int, dict] = None, access_token, query_params={}, version_string=None):
    url = f"{apiutils.getRestApiBaseUrl(version_string)}{resource}"

    headers = apiutils.getRestliRequestHeaders(
      restli_method=RESTLI_METHODS.GET,
      access_token=access_token,
      version_string=version_string
    )

    r = requests.get(url, params=query_params, headers=headers)

    return r.json()

  def batch_get(*, resource, ids, access_token, query_params={}, version_string=None):
    url = f"{apiutils.getRestApiBaseUrl(version_string)}{resource}"

    headers = apiutils.getRestliRequestHeaders(
      restli_method=RESTLI_METHODS.BATCH_GET,
      access_token=access_token,
      version_string=version_string
    )

    final_query_params = copy.deepcopy(query_params)
    final_query_params.update("ids", ids)

    r = requests.get(f"{url}?{encoder.encode_query_param_map(final_query_params)}", headers=headers)

    return r.json()

  def get_all(*, resource, access_token, query_params=None, version_string=None):
    url = f"{apiutils.getRestApiBaseUrl(version_string)}{resource}"

    if query_params:
      url += f"?{encoder.encode_query_param_map(query_params)}"

    headers = apiutils.getRestliRequestHeaders(
      restli_method=RESTLI_METHODS.GET_ALL,
      access_token=access_token,
      version_string=version_string
    )

    r = requests.get(url, headers=headers)

    return r.json()

  def finder(*, resource, finder_name, access_token, query_params={}, version_string=None):
    url = f"{apiutils.getRestApiBaseUrl(version_string)}{resource}"

    query_params_final = copy.deepcopy(query_params)
    query_params_final.update({"q": finder_name})

    headers = apiutils.getRestliRequestHeaders(
      restli_method=RESTLI_METHODS.FINDER,
      access_token=access_token,
      version_string=version_string
    )

    r = requests.get(url, params=encoder.param_encode(query_params_final), headers=headers)

    return r.json()

  def batch_finder(*, resource, batch_finder_name, access_token, query_params={}, version_string=None):
    url = f"{apiutils.getRestApiBaseUrl(version_string)}{resource}"

    final_query_params = copy.deepcopy(query_params)
    final_query_params.update("bq", batch_finder_name)
    encoded_query_param_string = encoder.encode_query_param_map(final_query_params)
    if encoded_query_param_string:
      url += f"?{encoded_query_param_string}"

    headers = apiutils.getRestliRequestHeaders(
      restli_method=RESTLI_METHODS.BATCH_FINDER,
      access_token=access_token,
      version_string=version_string
    )

    r = requests.get(url, headers=headers)

  def create(*, resource, entity, access_token, query_params=None, version_string=None):
    url = f"{apiutils.getRestApiBaseUrl(version_string)}{resource}"

    encoded_query_param_string = encoder.encode_query_param_map(query_params)

    if encoded_query_param_string:
      url += f"?{encoded_query_param_string}"

    headers = apiutils.getRestliRequestHeaders(
      restli_method=RESTLI_METHODS.CREATE,
      access_token=access_token,
      version_string=version_string
    )

    r = requests.post(url, headers=headers, json=entity)


  def batch_create(*, resource, entities, access_token, query_params={}, version_string=None):
    base_url = apiutils.getRestApiBaseUrl(version_string)
    encoded_query_param_string = encoder.param_encode(query_params)

    url = f"{base_url}{resource}"
    if encoded_query_param_string:
      url += f"?{encoded_query_param_string}"

    headers = apiutils.getRestliRequestHeaders(
      restli_method=RESTLI_METHODS.BATCH_CREATE,
      access_token=access_token,
      version_string=version_string
    )

    r = requests.post(url, headers=headers, json={
      "elements": entities
    })

  def update(*, resource, id=None, entity, access_token, query_params={}, version_string=None):
    """
    Makes a Rest.li UPDATE request to update an entity (overwriting the entire entity).

    :param str resource: The resource path (e.g. "/adAccounts").
    :param id:
    :param entity:
    :param query_params:
    :param access_token:
    :param version_string:
    :return:
    """
    base_url = apiutils.getRestApiBaseUrl(version_string)
    url = f"{base_url}{resource}"
    if id is not None:
      url += f"/{encoder.encode(id)}"

    encoded_query_param_string = encoder.param_encode(query_params)
    if encoded_query_param_string:
      url += f"?{encoded_query_param_string}"

    headers = apiutils.getRestliRequestHeaders(
      restli_method=RESTLI_METHODS.UPDATE,
      access_token=access_token,
      version_string=version_string
    )

    r = requests.put(url, headers=headers, json=entity)

  def batch_update():

  def partial_update():

  def batch_partial_update():

  def delete():

  def batch_delete():

  def action():