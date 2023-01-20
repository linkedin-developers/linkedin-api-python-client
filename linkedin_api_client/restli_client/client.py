import requests
import copy
from typing import Union, Dict, Any, List, Optional, Type, Tuple
import linkedin_api_client.utils.api as apiutils
import linkedin_api_client.utils.encoder as encoder
from linkedin_api_client.utils.restli import encode_query_params_for_get_requests
from linkedin_api_client.utils.query_tunneling import maybe_apply_query_tunneling_get_requests, maybe_apply_query_tunneling_requests_with_body
from linkedin_api_client.common.constants import RESTLI_METHODS
from linkedin_api_client.restli_client.response_formatter import ActionResponseFormatter, BatchCreateResponseFormatter, \
    BatchDeleteResponseFormatter, BatchFinderResponseFormatter, CollectionResponseFormatter, BatchGetResponseFormatter, \
    CreateResponseFormatter, GetResponseFormatter, BatchUpdateResponseFormatter, ResponseFormatter, UpdateResponseFormatter
from linkedin_api_client.restli_client.response import ActionResponse,BaseRestliResponse, BatchCreateResponse, \
    BatchDeleteResponse, BatchFinderResponse, BatchUpdateResponse, CreateResponse, GetResponse, \
    BatchGetResponse, CollectionResponse, RestliEntity, UpdateResponse

RestliEntityId = Union[str, int, Dict[str, Any]]


class RestliClient:
    def __init__(self, hooks: Optional[Dict[str, List[Any] | Any]]):
        self.session = requests.Session()
        if hooks is not None:
            self.session.hooks = hooks

    def get(
            self, *,
            resource_path: str,
            access_token: str,
            path_keys: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = {},
            version_string: Optional[str] = None) -> GetResponse:

        encoded_query_param_string = encode_query_params_for_get_requests(
            query_params)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.GET,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            version_string=version_string,
            formatter=GetResponseFormatter
        )

    def batch_get(self, *,
                  resource_path: str,
                  ids: List[RestliEntityId],
                  access_token: str,
                  path_keys: Optional[Dict[str, Any]] = None,
                  query_params: Optional[Dict[str, Any]] = None,
                  version_string: Optional[str] = None
                  ) -> BatchGetResponse:
        query_params_final = copy.deepcopy(
            query_params) if query_params else {}

        query_params_final.update({"ids": ids})
        encoded_query_param_string = encode_query_params_for_get_requests(
            query_params_final)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.BATCH_GET,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            version_string=version_string,
            formatter=BatchGetResponseFormatter
        )

    def get_all(self, *,
                resource_path: str,
                access_token: str,
                path_keys: Optional[Dict[str, Any]] = None,
                query_params: Optional[Dict[str, Any]] = None,
                version_string: Optional[str] = None
                ) -> CollectionResponse:

        encoded_query_param_string = encode_query_params_for_get_requests(
            query_params)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.GET_ALL,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            version_string=version_string,
            formatter=CollectionResponseFormatter
        )

    def finder(self, *,
               resource_path: str,
               finder_name: str,
               access_token: str,
               path_keys: Optional[Dict[str, Any]],
               query_params: Optional[Dict[str, Any]] = None,
               version_string: Optional[str] = None
               ) -> CollectionResponse:

        final_query_params = copy.deepcopy(
            query_params) if query_params else {}
        final_query_params.update({"q": finder_name})
        encoded_query_param_string = encode_query_params_for_get_requests(
            final_query_params)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.FINDER,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            version_string=version_string,
            formatter=CollectionResponseFormatter
        )

    def batch_finder(self, *,
                     resource_path: str,
                     finder_name: str,
                     finder_criteria: Tuple[str, List[Dict[str, Any]]],
                     access_token: str,
                     path_keys: Optional[Dict[str, Any]] = None,
                     query_params: Optional[Dict[str, Any]] = None,
                     version_string: Optional[str] = None
                     ) -> BatchFinderResponse:

        final_query_params = copy.deepcopy(
            query_params) if query_params else {}
        final_query_params.update({"bq": finder_name})
        final_query_params.update({finder_criteria[0]: finder_criteria[1]})
        encoded_query_param_string = encode_query_params_for_get_requests(
            final_query_params)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.BATCH_FINDER,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            version_string=version_string,
            formatter=BatchFinderResponseFormatter
        )

    def create(self, *,
               resource_path: str,
               entity: RestliEntity,
               access_token: str,
               path_keys: Optional[Dict[str, Any]] = None,
               query_params: Optional[Dict[str, Any]] = None,
               version_string: Optional[str] = None) -> CreateResponse:

        encoded_query_param_string = encoder.param_encode(query_params)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.CREATE,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            request_body=entity,
            version_string=version_string,
            formatter=CreateResponseFormatter
        )

    def batch_create(
            self,
            *,
            resource_path: str,
            entities: List[RestliEntity],
            access_token: str,
            path_keys: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = None,
            version_string: Optional[str] = None) -> BatchCreateResponse:

        encoded_query_param_string = encoder.param_encode(query_params)
        request_body = {
            "elements": entities
        }

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.BATCH_CREATE,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            request_body=request_body,
            version_string=version_string,
            formatter=BatchCreateResponseFormatter
        )

    def update(
            self,
            *,
            resource_path: str,
            entity: RestliEntity,
            access_token: str,
            path_keys: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = None,
            version_string: Optional[str] = None) -> UpdateResponse:

        encoded_query_param_string = encoder.param_encode(query_params)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.UPDATE,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            request_body=entity,
            version_string=version_string,
            formatter=UpdateResponseFormatter
        )

    def batch_update(
            self,
            *,
            resource_path: str,
            entities: List[RestliEntity],
            ids: List[RestliEntityId],
            access_token: str,
            path_keys: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = {},
            version_string: Optional[str] = None) -> BatchUpdateResponse:

        final_query_params = copy.deepcopy(
            query_params) if query_params else {}
        final_query_params.update({"ids": ids})
        encoded_query_param_string = encoder.param_encode(final_query_params)

        encoded_ids = [encoder.encode(id) for id in ids]
        entities_map = dict(zip(encoded_ids, entities))
        request_body = {
            "entities": entities_map
        }

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.BATCH_UPDATE,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            request_body=request_body,
            access_token=access_token,
            version_string=version_string,
            formatter=BatchUpdateResponseFormatter
        )

    def partial_update(
            self,
            *,
            resource_path: str,
            patch_set_object: Dict[str, Any],
            access_token: str,
            path_keys: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = None,
            version_string: Optional[str] = None) -> UpdateResponse:

        encoded_query_param_string = encoder.param_encode(query_params)

        request_body = {
            "patch": {
                "$set": patch_set_object
            }
        }

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.PARTIAL_UPDATE,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            request_body=request_body,
            access_token=access_token,
            version_string=version_string,
            formatter=UpdateResponseFormatter
        )

    def batch_partial_update(
            self,
            *,
            resource_path: str,
            ids: List[RestliEntityId],
            patch_set_objects: List[Dict[str, Any]],
            access_token: str,
            path_keys: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = None,
            version_string: Optional[str] = None) -> BatchUpdateResponse:

        final_query_params = copy.deepcopy(
            query_params) if query_params else {}
        final_query_params.update({"ids": ids})
        encoded_query_param_string = encoder.param_encode(final_query_params)

        entities_map = dict(zip(ids, patch_set_objects))
        request_body = {
            encoder.encode(id): {"patch": {"$set": patch_set_object}}
            for (id, patch_set_object) in entities_map.items()}

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.BATCH_PARTIAL_UPDATE,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            request_body=request_body,
            access_token=access_token,
            version_string=version_string,
            formatter=BatchUpdateResponseFormatter
        )

    def delete(
            self,
            *,
            resource_path: str,
            access_token: str,
            path_keys: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = {},
            version_string: Optional[str] = None) -> BaseRestliResponse:

        encoded_query_param_string = encoder.param_encode(query_params)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.DELETE,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            version_string=version_string,
            formatter=ResponseFormatter
        )

    def batch_delete(
        self,
        *,
        resource_path: str,
        ids: List[RestliEntityId],
        access_token: str,
        path_keys: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = {},
        version_string: Optional[str] = None
    ) -> BatchDeleteResponse:
        final_query_params = copy.deepcopy(
            query_params) if query_params else {}
        final_query_params.update({"ids": ids})
        encoded_query_param_string = encoder.param_encode(final_query_params)

        return self.__send_and_format_response(
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            restli_method=RESTLI_METHODS.BATCH_DELETE,
            access_token=access_token,
            version_string=version_string,
            formatter=BatchDeleteResponseFormatter
        )

    def action(
        self,
        *,
        resource_path: str,
        access_token: str,
        data: Any,
        path_keys: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        version_string: Optional[str] = None
    ) -> ActionResponse:

        encoded_query_param_string = encoder.param_encode(query_params)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.ACTION,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            request_body=data,
            access_token=access_token,
            version_string=version_string,
            formatter=ActionResponseFormatter
        )

    def __send_and_format_response(
        self,
        *,
        restli_method: RESTLI_METHODS,
        resource_path: str,
        access_token: str,
        formatter: Type[ResponseFormatter],
        path_keys: Optional[Dict[str, Any]] = None,
        encoded_query_param_string: Optional[str] = None,
        request_body: Optional[Any] = None,
        version_string: Optional[str] = None
    ) -> Type[BaseRestliResponse]:
        url = apiutils.build_rest_url(
            resource_path=resource_path,
            path_keys=path_keys,
            version_string=version_string
        )

        if request_body is not None:
            prepared_request = maybe_apply_query_tunneling_requests_with_body(
                encoded_query_param_string=encoded_query_param_string,
                url=url,
                original_restli_method=restli_method,
                original_request_body=request_body,
                access_token=access_token,
                version_string=version_string
            )
        else:
            prepared_request = maybe_apply_query_tunneling_get_requests(
                encoded_query_param_string=encoded_query_param_string,
                url=url,
                original_restli_method=restli_method,
                access_token=access_token,
                version_string=version_string
            )

        response = self.session.send(prepared_request)
        return formatter.format_response(response)
