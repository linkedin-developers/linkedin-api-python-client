import requests
import copy
from typing import Union, Dict, Any, List, Optional, Type, Tuple, TypeVar
from linkedin_api.clients.common.response import BaseResponse
import linkedin_api.clients.restli.utils.api as apiutils
import linkedin_api.clients.restli.utils.encoder as encoder
from linkedin_api.clients.restli.utils.restli import encode_query_params_for_get_requests
from linkedin_api.clients.restli.utils.query_tunneling import maybe_apply_query_tunneling_get_requests, maybe_apply_query_tunneling_requests_with_body
from linkedin_api.common.constants import RESTLI_METHODS
from linkedin_api.clients.restli.response_formatter import BaseResponseFormatter, ActionResponseFormatter, BatchCreateResponseFormatter, \
    BatchDeleteResponseFormatter, BatchFinderResponseFormatter, CollectionResponseFormatter, BatchGetResponseFormatter, \
    CreateResponseFormatter, GetResponseFormatter, BatchUpdateResponseFormatter, DeleteResponseFormatter, UpdateResponseFormatter
from linkedin_api.clients.restli.response import BaseRestliResponse, ActionResponse, BatchCreateResponse, \
    BatchDeleteResponse, BatchFinderResponse, BatchUpdateResponse, CreateResponse, GetResponse, \
    BatchGetResponse, CollectionResponse, RestliEntity, UpdateResponse

RestliEntityId = Union[str, int, Dict[str, Any]]

T = TypeVar('T', bound=BaseRestliResponse)

class RestliClient:
    """
    A client for making Rest.li-based, LinkedIn API calls.

    Attributes:
        session (requests.Session): The session instance used to send the API requests. Session attributes can
        be modified, which will affect all requests.
    """

    def __init__(self):
        """
        The constructor for the RestliClient class.
        """
        self.session = requests.Session()

    def get(
            self, *,
            resource_path: str,
            access_token: str,
            path_keys: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = {},
            version_string: Optional[str] = None) -> GetResponse:
        """
        Makes a Rest.li GET request to fetch the specified entity on a resource. This method will perform query
        tunneling if necessary.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            GetResponse: An instance of the GetResponse class representing the response from the Rest.li GET call

        Example:
            >>> response = restli_client.get(
                    resource_path="/adAccounts/{id}",
                    path_keys={ "id": 123 },
                    query_params={ "fields": "id,name" },
                    access_token=MY_ACCESS_TOKEN,
                    vesrion_string="202302"
                )
            >>> ad_account = response.entity
        """

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
        """
        Makes a Rest.li BATCH_GET request to fetch multiple entities on a resource. This method will perform query
        tunneling if necessary.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            ids (List[RestliEntityId]): The list of ids to fetch on a resource. These will be properly encoded by this method and added to the query parameters.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            BatchGetResponse: An instance of the BatchGetResponse class representing the response from the Rest.li BATCH_GET call

        Example:
            >>> response = restli_client.batch_get(
                    resource_path="/adCampaignGroups",
                    ids=[123, 456, 789],
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202302"
                )
            >>> campaign_groups = response.results.items()
        """
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
        """
        Makes a Rest.li GET_ALL request to fetch all entities on a resource.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            CollectionResponse: An instance of the CollectionResponse class representing the response from the Rest.li GET_ALL call

        Example:
            >>> response = restli_client.get_all(
                    resource_path="/fieldsOfStudy",
                    query_params={
                        "start": 0,
                        "count": 15
                    },
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202212"
                )
            >>> fields_of_study = response.elements
            >>> total = response.paging.total
        """
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
               path_keys: Optional[Dict[str, Any]] = None,
               query_params: Optional[Dict[str, Any]] = None,
               version_string: Optional[str] = None
               ) -> CollectionResponse:
        """
        Makes a Rest.li FINDER request to find entities by some specified criteria.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            finder_name (str): The Rest.li finder name. This will be added to the request query parameters.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            CollectionResponse: An instance of the CollectionResponse class representing the response from the Rest.li FINDER call

        Example:
            >>> response = restli_client.finder(
                    resource_path="/adAccounts",
                    finder_name="search",
                    query_params={
                        "search": {
                            "status": {
                                "values": ["ACTIVE", "DRAFT", "CANCELED"]
                            },
                            "test": False
                        },
                        "start": 0,
                        "count": 5
                    },
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202212"
                )
            >>> ad_accounts = response.elements
            >>> total = response.paging.total
        """

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
        """
        Makes a Rest.li BATCH_FINDER request to find entities by multiple sets of criteria.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            finder_name (str): The Rest.li batch finder name. This will be added to the request query parameters.
            finder_criteria (Tuple[str, List[Dict[str, Any]]]): The required batch finder criteria information. This is a tuple with the first value being the batch finder criteria parameter name. The second value is the list of finder param objects. The batch finder results are correspondingly ordered according to this list. The batch finder criteria will be encoded and added to the request query parameters.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            BatchFinderResponse: An instance of the BatchFinderResponse class representing the response from the Rest.li BATCH_FINDER call

        Example:
            >>> response = restli_client.batch_finder(
                    resource_path="/organizationAuthorizations",
                    finder_name="authorizationActionsAndImpersonator",
                    finder_criteria=("authorizationActions", [
                        {
                            "OrganizationRoleAuthorizationAction": {
                            actionType: "ADMINISTRATOR_READ"
                            }
                        },
                        {
                            "OrganizationContentAuthorizationAction": {
                            actionType: "ORGANIC_SHARE_DELETE"
                            }
                        }
                        ]
                    ),
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202212"
                )
            >>> admin_read_authorizations = response.results[0].elements
            >>> organic_share_delete_authorizations = response.results[1].elements
        """

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
        """
        Makes a Rest.li CREATE request to create a new resource entity.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            entity (RestliEntity): A dictionary representation of the entity to create.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            CreateResponse: An instance of the CreateResponse class representing the response from the Rest.li CREATE call

        Example:
            >>> response = restli_client.create(
                    resource_path="/adAccountsV2",
                    entity={
                        "name": "Test Ad Account",
                        "type": "BUSINESS",
                        "test": True
                    },
                    access_token=MY_ACCESS_TOKEN
                )
            >>> created_entity_id = response.entity_id
        """

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
        """
        Makes a Rest.li BATCH_CREATE request to create multiple entities in a single call.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            entities (List[RestliEntity]): A list of entities to create. Each entity is represented as a dictionary.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            BatchCreateResponse: An instance of the BatchCreateResponse class representing the response from the Rest.li BATCH_CREATE call

        Example:
            >>> response = restli_client.batch_create(
                    resource_path="/adCampaignGroups",
                    entities=[
                        {
                            account: 'urn:li:sponsoredAccount:111',
                            name: 'CampaignGroupTest1',
                            status: 'DRAFT'
                        },
                        {
                            account: 'urn:li:sponsoredAccount:222',
                            name: 'CampaignGroupTest2',
                            status: 'DRAFT'
                        }
                    ],
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202302"
                )
            >>> created_elements = response.elements
            >>> first_created_element_id = response.elements[0].id
        """

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
        """
        Makes a Rest.li UPDATE request to update an entity (overwriting the entity with the provided value).

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            entity (RestliEntity): The value of the updated entity. This will completely overwrite the entity.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            UpdateResponse: An instance of the UpdateResponse class representing the response from the Rest.li UPDATE call

        Example:
            >>> response = restli_client.update(
                    resource_path="/adAccountUsers/{id}",
                    path_keys={
                        "id": {
                            "account": "urn:li:sponsoredAccount:123",
                            "user": "urn:li:person:foobar"
                        }
                    },
                    entity: {
                        "account": "urn:li:sponsoredAccount:123",
                        "user": "urn:li:person:foobar",
                        "role": "VIEWER"
                    },
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202302"
                )
            >>> status = response.status_code
        """

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
        """
        Makes a Rest.li BATCH_UPDATE request to update multiple entities in a single call.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            ids (List[RestliEntityId]): The ids of the entities to update. These will be properly encoded and added to the query parameters.
            entities (List[RestliEntity]): A list of entities to create. Each entity is represented as a dictionary.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            BatchUpdateResponse: An instance of the BatchUpdateResponse class representing the response from the Rest.li BATCH_UPDATE call

        Example:
            >>> response = restli_client.batch_update(
                    resource_path="/campaignConversions",
                    ids=[
                        { "campaign": "urn:li:sponsoredCampaign:123", "conversion": "urn:lla:llaPartnerConversion:456" },
                        { "campaign": "urn:li:sponsoredCampaign:123", "conversion": "urn:lla:llaPartnerConversion:789" }
                    ],
                    entities=[
                        { "campaign": "urn:li:sponsoredCampaign:123", "conversion": "urn:lla:llaPartnerConversion:456" },
                        { "campaign": "urn:li:sponsoredCampaign:123", "conversion": "urn:lla:llaPartnerConversion:789" }
                    ],
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202302"
                )
            >>> batch_results = response.results.items()
        """

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
        """
        Makes a Rest.li PARTIAL_UPDATE request to update part of an entity. Directly specify the patch object to send in the request.

        Note: While the Rest.li protocol supports very granular patch objects with setting and deletion of nested properties, most LinkedIn APIs only support partial update on the top-level fields of an entity.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            patch_set_object (Dict[str, Any]): The value of the entity with only the modified fields present. This will be sent directly in the request body as `patch: { $set: patch_set_object }`.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            UpdateResponse: An instance of the UpdateResponse class representing the response from the Rest.li PARTIAL_UPDATE call

        Example:
            >>> response = restli_client.partial_update(
                    resource_path="/adAccounts/{id}",
                    path_keys={ "id": 123 },
                    patch_set_object: {
                        "name": "TestAdAccountModified",
                        "reference": "urn:li:organization:456"
                    },
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202302"
                )
            >>> status = response.status_code
        """
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
        """
        Makes a Rest.li BATCH_PARTIAL_UPDATE request to update multiple entities at once, by only providing the fields of the entities that require updating.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            ids (List[RestliEntityId]): The list of entity ids to update. These will be encoded and added to the query parameters.
            patch_set_objects (List[Dict[str, Any]]): The list of entity values, represented as a dictionary, with only the modified fields present.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            BatchUpdateResponse: An instance of the BatchUpdateResponse class representing the response from the Rest.li BATCH_PARTIAL_UPDATE call

        Example:
            >>> response = restli_client.batch_partial_update(
                    resource_path="/adCampaignGroups",
                    ids=["123", "456"],
                    patch_set_objects: [
                        { "status": "ACTIVE" },
                        {
                            "runSchedule": {
                                "start": 1678029270721,
                                "end": 1679029270721
                            }
                        }
                    ],
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202212"
                )
            >>> result_status = response.results["123"].status
        """

        final_query_params = copy.deepcopy(
            query_params) if query_params else {}
        final_query_params.update({"ids": ids})
        encoded_query_param_string = encoder.param_encode(final_query_params)

        id_to_patch_map = dict(zip(ids, patch_set_objects))
        entities_map = {
            encoder.encode(id): {"patch": {"$set": patch_set_object}}
            for (id, patch_set_object) in id_to_patch_map.items()}
        request_body = {
            "entities": entities_map
        }

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
        """
        Makes a Rest.li DELETE request to delete an entity.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            BaseRestliResponse: An instance of the BaseRestliResponse class representing the response of the Rest.li DELETE call

        Example:
            >>> response = restli_client.delete(
                    resource_path="/adAccounts/{id}",
                    path_keys={ "id": 123 },
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202302"
                )
            >>> status_code = response.status_code
        """

        encoded_query_param_string = encoder.param_encode(query_params)

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.DELETE,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            access_token=access_token,
            version_string=version_string,
            formatter=DeleteResponseFormatter
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
        """
        Makes a Rest.li BATCH_DELETE request to delete multiple entities at once.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            ids (List[RestliEntityId]): The list of entity ids to delete. These will be encoded and added to the query parameters.
            access_token (str): The access token that should provide the application access to the specified API.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.

        Returns:
            BatchDeleteResponse: An instance of BatchDeleteResponse class representing the response of the Rest.li BATCH_DELETE call

        Example:
            >>> response = restli_client.batch_delete(
                    resource_path="/adAccounts",
                    ids=["123", "456"],
                    access_token=MY_ACCESS_TOKEN,
                    version_string="202302"
                )
            >>> status_code = response.results["123"].status
        """

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
        action_name: str,
        access_token: str,
        action_params: Optional[Dict[str,Any]] = None,
        path_keys: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        version_string: Optional[str] = None
    ) -> ActionResponse:
        """
        Makes a Rest.li ACTION request to perform an action on a specified resource. This method is flexible and generally used when the action does not fit within the standard behavior defined by the other Rest.li methods.

        Args:
            resource_path (str): The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.
            action_name (str): The action method name. This will be added to the query parameters.
            access_token (str): The access token that should provide the application access to the specified API.
            action_params (Optional[Dict[str,Any]], optional): An optional map of action parameters and their values. This will be sent in the request body. Defaults to None.
            path_keys (Optional[Dict[str, Any]], optional): If there are path key placeholders as part of the `resource_path` argument, the key placeholders must be specified in this `path_keys` dictionary. The path key values can be strings, numbers, or objects, and these will be properly encoded. Defaults to None.
            query_params (Optional[Dict[str, Any]], optional): A dictionary of query parameters, where the key is the query parameter name, and the value is the query parameter value. This method will properly encode the query parameters. Defaults to {}.
            version_string (Optional[str], optional): A version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL. Defaults to None.


        Returns:
            ActionResponse: An instance of ActionResponse class representing the response of the Rest.li ACTION call

        Example:
            >>> response = restli_client.action(
                    resource_path="/liveAssetActions",
                    action_name="register",
                    action_params={
                        "registerLiveEventRequest": {
                            "owner": "urn:li:person:12345",
                            "recipes": ["urn:li:digitalmediaRecipe:feedshare-live-video"],
                            "region": "WEST_US"
                        }
                    },
                    access_token=MY_ACCESS_TOKEN
                )
            >>> status_code = response.status_code
        """
        final_query_params = copy.deepcopy(
            query_params) if query_params else {}
        final_query_params.update({ "action": action_name })

        encoded_query_param_string = encoder.param_encode(final_query_params)

        request_body = action_params if action_params else {}

        return self.__send_and_format_response(
            restli_method=RESTLI_METHODS.ACTION,
            resource_path=resource_path,
            path_keys=path_keys,
            encoded_query_param_string=encoded_query_param_string,
            request_body=request_body,
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
        formatter: Type[BaseResponseFormatter[T]],
        path_keys: Optional[Dict[str, Any]] = None,
        encoded_query_param_string: Optional[str] = None,
        request_body: Optional[Any] = None,
        version_string: Optional[str] = None
    ) -> T:
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
