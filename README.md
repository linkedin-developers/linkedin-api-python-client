# LinkedIn API Python Client

## Overview

This library provides a thin Python client for making requests to LinkedIn APIs, utilizing the Python [requests](https://pypi.org/project/requests/) HTTP client library. LinkedIn's APIs are built on the [Rest.li](https://linkedin.github.io/rest.li/) framework with additional LinkedIn-specific constraints, which results in a robust yet complex protocol that can be challenging to implement correctly.

This library helps reduce this complexity by formatting requests correctly, providing proper request headers, and providing interfaces to develop against for responses. The library also provides an auth client for inspecting, generating, and refreshing access tokens, along with other helpful utilities.

> :warning: This API client library is currently in beta and is subject to change. It may contain bugs, errors, or other issues that we are working to resolve. Use of this library is at your own risk. Please use caution when using it in production environments and be prepared for the possibility of unexpected behavior. We welcome any feedback or reports of issues that you may encounter while using this library.

### Features

- Generic support for all Rest.li methods used in LinkedIn APIs
- Supports Rest.li protocol version 2.0.0
- Provide interfaces for request options/response payloads
- Built-in parameter encoding
- Utilities (e.g. URN handling, encoding)
- Supports versioned APIs
- Automatic query tunneling of requests
- 2-legged and 3-legged OAuth2 support

### Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Pre-requisites](#pre-requisites)
  - [Simple API Request Example](#simple-api-request-example)
  - [Finder Request Example](#finder-request-example)
  - [More Examples](#more-examples)
- [API Reference](#api-reference)
  - [RestliClient](#class-restliclient)
    - [Constructor](#constructor)
    - [Properties](#properties)
    - [Methods](#methods)
      - [`get()`](#get-resource_path-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`batch_get()`](#batch_get-resource_path-ids-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`get_all()`](#get_all-resource_path-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`finder()`](#finder-resource_path-finder_name-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`batch_finder()`](#batch_finder-resource_path-finder_name-finder_criteria-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`create()`](#create-resource_path-entity-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`batch_create()`](#batch_create-resource_path-entities-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`update()`](#update-resource_path-entity-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`batch_update()`](#batch_update-resource_path-ids-entities-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`partial_update()`](#partial_update-resource_path-patch_set_object-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`batch_partial_update()`](#batch_partial_update-resource_path-ids-patch_set_objects-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`delete()`](#delete-resource_path-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`batch_delete()`](#batch_delete-resource_path-ids-access_token-path_keysnone-query_paramsnone-version_stringnone)
      - [`action()`](#action-resource_path-action_name-access_token-action_paramsnone-path_keysnone-query_paramsnone-version_stringnone)
  - [AuthClient](#class-authclient)
    - [Constructor](#constructor-1)
    - [Properties](#properties-1)
    - [Methods](#methods-1)
      - [`generate_member_auth_url()`](#generate_member_auth_url-scopes-statenone)
      - [`exchange_auth_code_for_access_token()`](#exchange_auth_code_for_access_token-code)
      - [`exchange_refresh_token_for_access_token()`](#exchange_refresh_token_for_access_token-refresh_token)
      - [`get_two_legged_access_token()`](#get_two_legged_access_token-)
      - [`introspect_access_token()`](#introspect_access_token-access_token)
- [List of dependencies](#list-of-dependencies)


## Requirements

- Python >= 3.7


## Installation

```sh
pip install linkedin-api-client
```

## Getting Started

### Pre-requisites

1. Create or use an existing developer application from the [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps/)
2. Request access to the Sign In With LinkedIn API product. This is a self-serve product that will be provisioned immediately to your application.
3. Generate a 3-legged access token using the Developer Portal [token generator tool](https://www.linkedin.com/developers/tools/oauth/token-generator), selecting the r_liteprofile scope.

### Simple API Request Example

Here is an example of using the client to make a simple GET request to [fetch the current user's profile](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin#retrieving-member-profiles). This requires a 3-legged access token with the "r_liteprofile" scope, which is included with the Sign In With LinkedIn API product.

```python
from linkedin_api.clients.restli.client import RestliClient

restli_client = RestliClient()

response = restli_client.get(
  resource_path="/me",
  access_token=<THREE_LEGGED_ACCESS_TOKEN>
)
print(response.entity)
```

### Finder Request Example

Here is a more non-trivial example to [find ad accounts](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-accounts?#search-for-accounts) by some search critiera. This requires a 3-legged access token with the "r_ads" scope, which is included with the Advertising APIs product.

The "search" query parameter in this case is not a primitive, but a complex object, which we represent as a dictionary. The client will handle the correct URL-encoding. This is a versioned API call, so we also need to provide the version string in the "YYYYMM" format.

```python
from linkedin_api.clients.restli.client import RestliClient

restli_client = RestliClient()

response = restli_client.finder(
  resource_path="/adAccounts",
  finder_name="search",
  query_params={
    "search": {
      "status": {
        "values": ["ACTIVE", "DRAFT"]
      },
      "reference": {
        "values": ["urn:li:organization:123"]
      },
      "test": True
    }
  },
  version_string="202212",
  acccess_token=<THREE_LEGGED_ACCESS_TOKEN>
)
ad_accounts = response.elements
```

### More Examples

There are more examples of using the client in [/examples](examples/) directory.


## API Reference

### `class RestliClient`

The Rest.li API client defines instance methods for all the Rest.li methods which are used by LinkedIn APIs. All calls are blocking.

Rest.li defines a standard set of methods that can operate on a resource, each of which maps to an HTTP method. Depending on the resource, some Rest.li methods are not applicable or not implemented. Read the API docs to determine what Rest.li method is applicable and the relevant request parameters.

#### Constructor

An instance of the API client must be created before using. This creates a session object that will be used for making all subsequent requests.

```python
from linkedin_api.clients.restli.client import RestliClient

restli_client = RestliClient()
```

The Requests library [session](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) object is accessible to configure any additional global settings (e.g. configuring event hooks).

```python
restli_client.session.hooks = { 'response': [do_something_fn, do_something_2_fn] }
```

#### Properties

| Property | Description |
|---|---|
| `session` | The session object used for making http requests. This is exposed to allow for additional configuration (e.g. adding custom request/response event hooks). |

#### Methods

##### Base Request Parameters

All Rest.li request methods of the API client support the following request parameters:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `resource_path` | str | Yes | <p>The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.</p><p>Examples:</p><ul><li>`resource_path="/me"`</li><li>`resource_path="/adAccounts/{id}"`</li><li>`resource_path="/socialActions/{actionUrn}/comments/{commentId}"`</li><li>`resource_path="/campaignConversions/{key}`</li></ul>|
| `access_token` | str | Yes | The access token that should provide the application access to the specified API |
| `path_keys` | Dict[str,Any] | No | <p>If there are path keys that are part of the `resource_path` argument, the key placeholders must be specified in the provided `path_keys` map. The path key values can be strings, numbers, or objects (dictionaries), and these will be properly encoded.</p><p>Examples:</p><p><ul><li>`path_keys={"id": 123"}`</li><li>`path_keys={"actionUrn":"urn:li:share:123","commentId":987`}</li><li>`path_keys={"key": {"campaign": "urn:li:sponsoredCampaign:123", "conversion": "urn:lla:llaPartnerConversion:456"}}`</li></ul></p> |
| `query_params` | Dict[str,Any] | No | A map of query parameters. The query parameter values (strings, lists, objects) will be correctly encoded by this method, so these should not be encoded. |
| `version_string` | str | No | An optional version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL |

##### `get (resource_path, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li GET request to fetch the specified entity on a resource. This method will perform query tunneling if necessary.

**Parameters:**

This method only uses the [base request parameters](#base-request-parameters) defined above.

**Return value:**

Returns [GetResponse](#class-getresponse) object

**Example:**

```python
response = restli_client.get(
  resource_path="/adAccounts/{id}"
  path_keys={ "id": 123 },
  query_params={ "fields": "id,name" }
  access_token=MY_ACCESS_TOKEN,
  version_string="202212"
)
ad_account = response.entity
```


##### `batch_get (resource_path, ids, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li BATCH_GET request to fetch multiple entities on a resource. This method will perform query tunneling if necessary.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `ids` | List[Union[str,int,Dict[str,Any]]] | Yes | The list of entity ids to fetch on the resource. These will be encoded and added to the query parameters. |

**Return value:**

Returns a [BatchGetResponse](#class-batchgetresponse) object.

**Example:**

```python
response = restli_client.batch_get(
  resource_path="/adCampaignGroups",
  ids=[123, 456, 789],
  access_token=MY_ACCESS_TOKEN,
  version_string="202212"
)
campaign_groups = response.results.items()
```


##### `get_all (resource_path, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li GET_ALL request to fetch all entities on a resource.

**Parameters:**

This method only uses the [base request parameters](#base-request-parameters) defined above.

**Return value:**

Returns [CollectionResponse](#class-collectionresponse) object

**Example:**

```python
response = restli_client.get_all(
  resource_path="/fieldsOfStudy",
  query_params={
    "start": 0,
    "count": 15
  },
  access_token=MY_ACCESS_TOKEN,
  version_string="202212"
)
fields_of_study = response.elements
total = response.paging.total
```

##### `finder (resource_path, finder_name, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li FINDER request to find entities by some specified criteria.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `finder_name` | str | Yes | The Rest.li finder name. This will be added to the request query parameters. |

**Return value:**

Returns a [CollectionResponse](#class-collectionresponse) object.

**Example:**

```python
response = restli_client.finder(
  resource_path="/adAccounts",
  finder_name="search",
  query_params={
    "search": {
        "status": {
            "values": ["ACTIVE", "DRAFT", "CANCELED"]
        },
        "reference": {
            "values": ["urn:li:organization:123"]
        },
        "test": False
    },
    "start": 0,
    "count": 5
  },
  access_token=MY_ACCESS_TOKEN,
  version_string="202212"
)
ad_accounts = response.elements
total = response.paging.total
```

##### `batch_finder (resource_path, finder_name, finder_criteria, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li BATCH_FINDER request to find entities by multiple sets of criteria.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `finder_name` | str | Yes | The Rest.li batch finder name (the value of the "bq" query parameter). This will be added to the request query parameters. |
| `finder_criteria` | Tuple[str, List[Dict[str,Any]]] | Yes | The required batch finder criteria information. This is a tuple with the first value being the batch finder criteria parameter name. The second value is the list of finder param objects. The batch finder results are correspondingly ordered according to this list. The batch finder criteria will be encoded and added to the request query parameters. |

**Return value:**

Returns a [BatchFinderResponse](#class-batchfinderresponse) object.

**Example:**

```python
response = restli_client.batch_finder(
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
admin_read_authorizations = response.results[0].elements
organic_share_delete_authorizations = response.results[1].elements
```

##### `create (resource_path, entity, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li CREATE request to create a new resource entity.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `entity` | Dict[str,Any] | Yes | A dictionary representation of the entity to create |

**Return value:**

Returns a [CreateResponse](#class-createresponse) object.

**Example:**

```python
response = restli_client.create(
  resource_path="/adAccountsV2",
  entity={
    "name": "Test Ad Account",
    "type": "BUSINESS",
    "test": True
  },
  access_token=MY_ACCESS_TOKEN
)
created_entity_id = response.entity_id
```

##### `batch_create (resource_path, entities, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li BATCH_CREATE request to create multiple entities in a single call.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `entities` | List[Dict[str,Any]] | Yes | A list of entities to create |

**Return value:**

Returns a [BatchCreateResponse](#class-batchcreateresponse) object.

**Example:**

```python
response = restli_client.batch_create(
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
  version_string="202212"
)
created_elements = response.elements
first_created_element_id = response.elements[0].id
```

##### `update (resource_path, entity, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li UPDATE request to update an entity (overwriting the entity with the provided value).

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `entity` | Dict[str,Any] | Yes | The value of the updated entity. This will completely overwrite the entity. |

**Return value:**

Returns a [UpdateResponse](#class-updateresponse) object.

**Example:**

```python
response = restli_client.update(
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
  version_string="202212"
)
status = response.status_code
```

##### `batch_update (resource_path, ids, entities, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li BATCH_UPDATE request to update multiple entities in a single call.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `ids` | List[Union[str,int,Dict[str,Any]]] | Yes | The ids of the entities to update |
| `entities` | List[Dict[str,Any]] | Yes | The values to update the specified entities to. This should be the same order as the `ids` argument. |

**Return value:**

Returns a [BatchUpdateResponse](#class-batchupdateresponse) object.

**Example:**

```python
response = restli_client.batch_update(
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
  version_string="202212"
)
batch_results = response.results.items()
```

##### `partial_update (resource_path, patch_set_object, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li PARTIAL_UPDATE request to update part of an entity. Directly specify the patch object to send in the request.

Note: While the Rest.li protocol supports very granular patch objects with setting and deletion of nested properties, most LinkedIn APIs only support partial update on the top-level fields of an entity.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `patch_set_object` | Dict[str,Any] | Yes | The value of the entity with only the modified fields present. This will be sent directly in the request body as `patch: { $set: patch_set_object }`. |

**Return value:**

Returns a [UpdateResponse](#class-updateresponse) object.

**Example:**

```python
response = restli_client.partial_update(
  resource_path="/adAccounts/{id}",
  path_keys={ "id": 123 },
  patch_set_object: {
    "name": "TestAdAccountModified",
    "reference": "urn:li:organization:456"
  },
  access_token=MY_ACCESS_TOKEN,
  version_string="202212"
)
status = response.status_code
```

##### `batch_partial_update (resource_path, ids, patch_set_objects, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li BATCH_PARTIAL_UPDATE request to update multiple entities at once, by only providing the fields of the entities that require updating.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `ids` | List[Union[str,int,Dict[str,Any]]] | Yes | The list of entity ids to update. These will be encoded and added to the query parameters. |
| `patch_set_objects` | List[Dict[str,Any]] | Yes | The list of entity values, represented as a dictionary, with only the modified fields present. |

**Return value:**

Returns a [BatchUpdateResponse](#class-batchupdateresponse) object.

**Example:**

```python
response = restli_client.batch_partial_update(
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
result_status = response.results["123"].status
```

##### `delete (resource_path, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li DELETE request to delete an entity.

**Parameters:**

This method only uses the [base request parameters](#base-request-parameters) defined above.

**Return value:**

Returns [BaseRestliResponse](#class-baserestliresponse) object

**Example:**

```python
response = restli_client.delete(
  resource_path="/adAccounts/{id}",
  path_keys={ "id": 123 },
  access_token=MY_ACCESS_TOKEN,
  version_string="202212"
)
status_code = response.status_code
```

##### `batch_delete (resource_path, ids, access_token, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li BATCH_DELETE request to delete multiple entities at once.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `ids` | List[Union[str,int,Dict[str,Any]]] | Yes | The list of entity ids to delete. These will be encoded and added to the query parameters. |

**Return value:**

Returns [BatchDeleteResponse](#class-batchdeleteresponse) object

**Example:**

```python
response = restli_client.batch_delete(
  resource_path="/adAccounts",
  ids=["123", "456"],
  access_token=MY_ACCESS_TOKEN,
  version_string="202212"
)
status_code = response.results["123"].status
```

##### `action (resource_path, action_name, access_token, action_params=None, path_keys=None, query_params=None, version_string=None)`

Makes a Rest.li ACTION request to perform an action on a specified resource. This method is flexible and generally used when the action does not fit within the standard behavior defined by the other Rest.li methods.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `action_name` | str | Yes | The action method name. This will be added to the query parameters. |
| `action_params` | Dict[str,Any] | No | An optional map of action parameters and their values. This will be sent in the request body. |

**Return value:**

Returns [ActionResponse](#class-actionresponse) object

**Example:**

```python
response = restli_client.action(
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
status_code = response.status_code
```

#### Response Classes

##### `class BaseRestliResponse`

All Rest.li request methods of the API client return a response object subclassed from BaseRestliResponse, containing standard response data, along with the original, raw response object.

| Properties | Type | Description |
|---|---|---|
| `status_code` | int | Response status code |
| `url` | str | The final URL location of the response |
| `headers` | CaseInsensitiveDict | A case-insensitive dictionary of response headers |
| `response` | Response | The raw requests.Response object |

##### `class Paging`

Paging metadata class

| Properties | Type | Description |
|---|---|---|
| start | int | The start index of returned results (zero-based index) |
| count | int | The number of results returned in the response |
| total | int | The total number of results available |

##### `class GetResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `entity` | Union[Dict[str,Any], str, int, bool] | The representation (typically a dictionary) of the retrieved entity, decoded from the json-encoded response content |

##### `class BatchGetResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `results` | Dict[str,Any] | A map of entities that were successfully retrieved, with the key being the encoded entity id, and the value being a dictionary representing the entity |
| `statuses` | Dict[str,int] | A map of entities and status code, with the key being the encoded entity id, and the value being the status code number value. |
| `errors` | Dict[str,Any] | A map containing entities that could not be successfully fetched, with the key being the encoded entity id, and the value being the error response. |

##### `class CollectionResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `elements` | List[Dict[str,Any]] | The list of entities returned in the response |
| `paging` | [Paging](#class-paging) | Optional paging metadata object |
| `metadata` | Any | Optional response metadata object |

##### `class BatchFinderResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `results` | List[[BatchFinderResult](#class-batchfinderresult)] | The list of finder results, in the same order as the requested batch finder search criteria list |

##### `class BatchFinderResult`

| Properties | Type | Description |
|---|---|---|
| `elements` | List[Dict[str,Any]] | The list of entities found for the corresponding finder criteria |
| `paging` | [Paging](#class-paging) | Optional paging metadata object |
| `metadata` | Any | Optional response metadata object |
| `error` | Any | Optional error details if finder call failed |
| `isError` | bool | Flag if this finder call experienced an error |

##### `class CreateResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `entity_id` | str | The encoded entity id |
| `entity` | Dict[str,Any] | Optional created entity. Some APIs support returning the created entity to eliminate the need for a subsequent GET call. |

##### `class BatchCreateResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `elements` | List[[BatchCreateResult](#class-batchcreateresult)] | The list of batch create results, corresponding to the order of the `entities` request parameter |

##### `class BatchCreateResult`

| Properties | Type | Description |
|---|---|---|
| `status` | int | The status code of the individual create call |
| `id` | str | The id of the created entity |
| `error` | Any | Error details if the create call experienced an error |

##### `class UpdateResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `entity` | Dict[str,Any] | Optional entity after the update. Some APIs support returning the updated entity to eliminate the need for a subsequent GET call. |

##### `class BatchUpdateResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `results` | Dict[str,[BatchUpdateResult](#class-batchupdateresult)] | The results map where the keys are the encoded entity ids, and the values are the individual update call results, which includes the status code. |

##### `class BatchUpdateResult`

| Properties | Type | Description |
|---|---|---|
| `status` | int | The status code of the individual update call |

##### `class BatchDeleteResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `results` | Dict[str,[BatchDeleteResult](#class-batchdeleteresult)] | The results map where the keys are the encoded entity ids, and the values are the individual delete call results, which includes the status code. |

##### `class BatchDeleteResult`

| Properties | Type | Description |
|---|---|---|
| `status` | int | The status code of the delete call |

##### `class ActionResponse`

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `value` | Any | The action response value |


### `class AuthClient`

While we recommend using any of several popular, open-source libraries for robustly managing OAuth 2.0 authentication, we provide a basic Auth Client as a convenience for testing APIs and getting started.

#### Constructor

```python
from linkedin_api.clients.auth.client import AuthClient

auth_client = AuthClient(client_id=MY_CLIENT_ID, client_secret=MY_CLIENT_SECRET, redirect_url=MY_REDIRECT_URL)
```

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `client_id` | str | Yes | Client ID of your developer application. This can be found on your application auth settings page in the Developer Portal. |
| `client_secret` | str | Yes | Client secret of your developer application. This can be found on your application auth settings page in the Developer Portal. |
| `redirect_url` | str | No | If your integration will be using the authorization code flow to obtain 3-legged access tokens, this should be provided. This redirect URL must match one of the redirect URLs configured in the app auth settings page in the Developer Portal. |

#### Properties

| Property | Description |
|---|---|
| `session` | The session object used for making http requests. This is exposed to allow for additional configuration (e.g. adding custom request/response event hooks). |

#### Methods

##### `generate_member_auth_url (scopes, state=None)`

Generates the member authorization URL to direct members to. Once redirected, the member will be presented with LinkedIn's OAuth consent page showing the OAuth scopes your application is requesting on behalf of the user.

**Parameters:**

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `scopes` | List[str] | Yes | An array of OAuth scopes (3-legged member permissions) your application is requesting on behalf of the user. |
| `state` | str | No | An optional string that can be provided to test against CSRF attacks. |

**Return value:**

The member authorization URL string

##### `exchange_auth_code_for_access_token (code)`

Exchanges an authorization code for a 3-legged access token. After member authorization, the browser redirects to the provided redirect URL, setting the authorization code on the `code` query parameter.

**Parameters:**

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `code` | str | Yes | The authorization code to exchange for an access token |

**Return value:**

Returns an [AccessToken3LResponse](#class-accesstoken3lresponse) object

##### `exchange_refresh_token_for_access_token (refresh_token)`

Exchanges a refresh token for a new 3-legged access token. This allows access tokens to be refreshed without having the member reauthorize your application.

**Parameters:**

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `refresh_token` | str | Yes | The authorization code to exchange for an access token |

**Return value:**

Returns a [RefreshTokenExchangeResponse](#class-refreshtokenexchangeresponse) object

##### `get_two_legged_access_token ()`

Use client credential flow (2-legged OAuth) to retrieve a 2-legged access token for accessing APIs that are not member-specific. Developer applications do not have the client credential flow enabled by default.

**Parameters:**

None

**Return value:**

Returns an [AccessToken2LResponse](#class-accesstoken2lresponse) object

##### `introspect_access_token (access_token)`

Introspect a 2-legged, 3-legged or Enterprise access token to get information on status, expiry, and other details.

**Parameters:**

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `access_token` | str | Yes | A 2-legged, 3-legged or Enterprise access token. |

**Return value:**

Returns an [IntrospectTokenResponse](#class-introspecttokenresponse) object


#### Response Classes

##### `class BaseAuthResponse`

All request methods of the AuthClient return a response object subclassed from BaseAuthResponse, containing standard response data, along with the original, raw response object.

| Properties | Type | Description |
|---|---|---|
| `status_code` | int | Response status code |
| `url` | str | The final URL location of the response |
| `headers` | CaseInsensitiveDict | A case-insensitive dictionary of response headers |
| `response` | Response | The raw requests.Response object |

##### `class AccessToken3LResponse`

Base class: [BaseAuthResponse](#class-baseauthresponse)

| Properties | Type | Description |
|---|---|---|
| `access_token` | str | The 3-legged access token |
| `expires_in` | int | The TTL of the access token, in seconds |
| `refresh_token` | str | The refresh token value. This is only present if refresh tokens are enabled for the application. |
| `refresh_token_expires_in` | Number | The TTL of the refresh token, in seconds. This is only present if refresh tokens are enabled for the application. |
| `scope` | str | A comma-separated list of scopes authorized by the member (e.g. "r_liteprofile,r_ads") |

##### `class AccessToken2LResponse`

Base class: [BaseAuthResponse](#class-baseauthresponse)

| Properties | Type | Description |
|---|---|---|
| `access_token` | str | The 2-legged access token |
| `expires_in` | int | The TTL of the access token, in seconds |

##### `class RefreshTokenExchangeResponse`

Base class: [BaseAuthResponse](#class-baseauthresponse)

| Properties | Type | Description |
|---|---|---|
| `access_token` | str | The 3-legged access token |
| `expires_in` | int | The TTL of the access token, in seconds |
| `refresh_token` | str | The refresh token value. This is only present if refresh tokens are enabled for the application. |
| `refresh_token_expires_in` | Number | The TTL of the refresh token, in seconds. This is only present if refresh tokens are enabled for the application. |


##### `class IntrospectTokenResponse`

Base class: [BaseAuthResponse](#class-baseauthresponse)

| Properties | Type | Description |
|---|---|---|
| `active` | str | Flag whether the token is a valid, active token. |
| `auth_type` | str | The auth type of the token ("2L", "3L" or "Enterprise_User") |
| `authorized_at` | str | Epoch time in seconds, indicating when the token was authorize |
| `client_id` | str | Developer application client ID |
| `created_at` | int | Epoch time in seconds, indicating when this token was originally issued |
| `expires_at` | int | Epoch time in seconds, indicating when this token will expire |
| `scope` | str | A string containing a comma-separated list of scopes associated with this token. This is only returned for 3-legged member tokens. |
| `status` | str | The token status, which is an enum string with values "revoked", "expired" or "active" |

---

## List of dependencies

The following table is a list of production dependencies.

| Component Name | License | Linked | Modified |
|---|---|---|---|
| [requests](https://pypi.org/project/requests/) | Apache 2.0 | Static | No |
