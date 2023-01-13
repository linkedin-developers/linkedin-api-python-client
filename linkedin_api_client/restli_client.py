import requests
import copy
from typing import Union, Dict, Any, List
import linkedin_api_client.utils.api as apiutils
import linkedin_api_client.utils.encoder as encoder
from linkedin_api_client.utils.restli import encode_query_params_for_get_requests
from linkedin_api_client.utils.query_tunneling import maybe_apply_query_tunneling_get_requests, maybe_apply_query_tunneling_requests_with_body
from linkedin_api_client.constants import RESTLI_METHODS
from linkedin_api_client.response_formatter import EntityResponseFormatter, BatchGetResponseFormatter
from linkedin_api_client.response import EntityResponse, BatchGetResponse

RestliEntityId = Union[str, int, Dict[str, Any]]


class RestliClient:
    def __init__(self):
        self.session = requests.Session()

    def get(self, *, resource_path_template: str, path_keys: Dict[str, Any] = None, access_token, query_params={}, version_string=None) -> EntityResponse:
        url = apiutils.build_rest_url(
            resource_path_template=resource_path_template,
            path_keys=path_keys,
            version_string=version_string
        )
        encoded_query_param_string = encode_query_params_for_get_requests(
            query_params)
        prepared_request = maybe_apply_query_tunneling_get_requests(
            encoded_query_param_string=encoded_query_param_string,
            url=url,
            original_restli_method=RESTLI_METHODS.GET.value,
            access_token=access_token,
            version_string=version_string
        )

        response = self.session.send(prepared_request)
        response.raise_for_status()

        return EntityResponseFormatter.format_response(response.json())

    def batch_get(self, *,
                  resource_path_template: str,
                  path_keys: Dict[str, Any] = None,
                  ids: List[RestliEntityId],
                  access_token: str,
                  query_params: Dict[str, Any] = {},
                  version_string: str = None
                  ) -> BatchGetResponse:
        url = apiutils.build_rest_url(
            resource_path_template=resource_path_template,
            path_keys=path_keys,
            version_string=version_string
        )
        query_params_final = copy.deepcopy(query_params)
        query_params_final.update({"ids": ids})
        encoded_query_param_string = encode_query_params_for_get_requests(query_params_final)
        prepared_request = maybe_apply_query_tunneling_get_requests(
          encoded_query_param_string=encoded_query_param_string,
          url=url,
          original_restli_method=RESTLI_METHODS.BATCH_GET.value,
          access_token=access_token,
          version_string=version_string
        )

        response = self.session.send(prepared_request)
        response.raise_for_status()

        return BatchGetResponseFormatter.format_response(response)

    def get_all(*, resource, access_token, query_params=None, version_string=None):
        url = f"{apiutils.getRestApiBaseUrl(version_string)}{resource}"

        if query_params:
            url += f"?{encoder.encode_query_param_map(query_params)}"

        headers = apiutils.getRestliRequestHeaders(
            restli_method=RESTLI_METHODS.GET_ALL.value,
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
            restli_method=RESTLI_METHODS.FINDER.value,
            access_token=access_token,
            version_string=version_string
        )

        r = requests.get(url, params=encoder.param_encode(
            query_params_final), headers=headers)

        return r.json()

    def batch_finder(*, resource, batch_finder_name, access_token, query_params={}, version_string=None):
        url = f"{apiutils.getRestApiBaseUrl(version_string)}{resource}"

        final_query_params = copy.deepcopy(query_params)
        final_query_params.update("bq", batch_finder_name)
        encoded_query_param_string = encoder.encode_query_param_map(
            final_query_params)
        if encoded_query_param_string:
            url += f"?{encoded_query_param_string}"

        headers = apiutils.getRestliRequestHeaders(
            restli_method=RESTLI_METHODS.BATCH_FINDER.value,
            access_token=access_token,
            version_string=version_string
        )

        r = requests.get(url, headers=headers)

    def create(*, resource, entity, access_token, query_params=None, version_string=None):
        url = f"{apiutils.getRestApiBaseUrl(version_string)}{resource}"

        encoded_query_param_string = encoder.encode_query_param_map(
            query_params)

        if encoded_query_param_string:
            url += f"?{encoded_query_param_string}"

        headers = apiutils.getRestliRequestHeaders(
            restli_method=RESTLI_METHODS.CREATE.value,
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
            restli_method=RESTLI_METHODS.BATCH_CREATE.value,
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
            restli_method=RESTLI_METHODS.UPDATE.value,
            access_token=access_token,
            version_string=version_string
        )

        r = requests.put(url, headers=headers, json=entity)

    def batch_update():
        pass

    def partial_update():
        pass

    def batch_partial_update():
        pass

    def delete():
        pass

    def batch_delete():
        pass

    def action():
        pass
