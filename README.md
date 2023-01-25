## Overview

This library provides a thin Python client for making requests to LinkedIn APIs, utilizing the Python [requests](https://pypi.org/project/requests/) HTTP client library. LinkedIn's APIs are built on the [Rest.li](https://linkedin.github.io/rest.li/) framework with additional LinkedIn-specific constraints, which results in a robust yet complex protocol that can be challenging to implement correctly.

This library helps reduce this complexity by formatting requests correctly, providing proper request headers, and providing interfaces to develop against for responses. The library also provides an auth client for inspecting, generating, and refreshing access tokens, along with other helpful utilities.

> :warning: This API client library is currently in beta and is subject to change. It may contain bugs, errors, or other issues that we are working to resolve. Use of this library is at your own risk. Please use caution when using it in production environments and be prepared for the possibility of unexpected behavior. We welcome any feedback or reports of issues that you may encounter while using this library.

### Features

- Generic support for all Rest.li methods used in LinkedIn APIs
- Supports Rest.li protocol version 2.0.0
- Provide typescript interfaces for request options/response payloads
- Built-in parameter encoding
- Partial update patch generation utilities
- LinkedIn URN utilities
- Supports versioned APIs
- Automatic query tunneling of requests
- 2-legged and 3-legged OAuth2 support

### Requirements

- Python >= 3.5


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
from linkedin_api_client.restli_client.client import RestliClient

restli_client = RestliClient()

response = restli_client.get(
  resource_path="/me",
  access_token=<THREE_LEGGED_ACCESS_TOKEN>
)
print(response.entity)
```

### Finder Request Example

Here is a more non-trivial example to [find ad accounts](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-accounts?#search-for-accounts) by some search critiera. This requires a 3-legged access token with the "r_ads" scope, which is included with the Marketing Developer Platform API product.

We provide the JSON-serialized value of the "search" query parameter object, and the client will handle the correct URL-encoding. This is a versioned API call, so we provide the version string in the "YYYYMM" format.

```python
from linkedin_api_client.restli_client.client import RestliClient

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


## API Client

The API client defines instance methods for all the Rest.li methods which are used by LinkedIn APIs. All calls are blocking.

Rest.li defines a standard set of methods that can operate on a resource, each of which maps to an HTTP method. Depending on the resource, some Rest.li methods are not applicable or not implemented. Read the API docs to determine what Rest.li method is applicable and the relevant request parameters.

### Constructor

An instance of the API client must be created before using. This creates a session object that will be used for making all subsequent requests.

```python
from linkedin_api_client.restli_client.client import RestliClient

restli_client = RestliClient()
```

The Requests libary [session](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) object is accessible to configure any additional global settings (e.g. configuring event hooks).

```
restli_client.session.hooks = { 'response': [do_something_fn, do_something_2_fn] }
```

### Properties

| Property | Description |
|---|---|
| `session` | The session object used for making http requests. This is exposed to allow for additional configuration (e.g. adding custom request/response event hooks). |

### Relevant Interfaces

#### Base Request Parameters

All Rest.li request methods of the API client support the following request parameters:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `resource_path` | str | Yes | <p>The resource path after the base URL, beginning with a forward slash. If the path contains keys, add curly-brace placeholders for the keys and specify the path key-value map in the `path_keys` argument.</p><p>Examples:</p><ul><li>`resource_path="/me"`</li><li>`resource_path="/adAccounts/{id}"`</li><li>`resource_path="/socialActions/{actionUrn}/comments/{commentId}"`</li><li>`resource_path="/campaignConversions/{key}`</li></ul>|
| `access_token` | str | Yes | The access token that should provide the application access to the specified API |
| `path_keys` | Dict[str,Any] | No | <p>If there are path keys that are part of the `resource_path` argument, the key placeholders must be specified in the provided `path_keys` map. The path key values can be strings, numbers, or objects (dictionaries), and these will be properly encoded.</p><p>Examples:</p><p><ul><li>`path_keys={"id": 123"\}`</li><li>`path_keys={"actionUrn":"urn:li:share:123","commentId":987`}</li><li>`path_keys={"key": {"campaign": "urn:li:sponsoredCampaign:123", "conversion": "urn:lla:llaPartnerConversion:456"}}`</li></ul></p> |
| `query_params` | Dict[str,Any] | No | A map of query parameters. The query parameter values (strings, lists, objects) will be correctly encoded by this method, so these should not be encoded. |
| `version_string` | str | No | An optional version string of the format "YYYYMM" or "YYYYMM.RR". If specified, the version header will be passed and the request will use the versioned APIs base URL |



### Methods

#### get *(resource_path, access_token, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li GET request to fetch the specified entity on a resource. This method will perform query tunneling if necessary.

**Parameters:**

This method only uses the [base request parameters](#base-request-parameters) defined above.

**Response:**

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


#### batch_get *(resource_path, ids, access_token, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li BATCH_GET request to fetch multiple entities on a resource. This method will perform query tunneling if necessary.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `ids` | List[Union[str,int,Dict[str,Any]]] | Yes | The list of entity ids to fetch on the resource. These will be encoded and added to the query parameters. |

**Response:**

Returns a [BatchGetResponse](#class-batchgetresponse) object.


**Example:**

```python
response = restli_client.batch_get(
  resource_path="/adCampaignGroups",
  ids=[123, 456, 789],
  access_token=MY_ACCESS_TOKEN,
  version_string="202212"
)
campaign_groups = response.resultsMap.items()
```


#### get_all *(resource_path, access_token, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li GET_ALL request to fetch all entities on a resource.

**Parameters:**

This method only uses the [base request parameters](#base-request-parameters) defined above.

**Response:**

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

#### finder *(resource_path, finder_name, access_token, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li FINDER request to find entities by some specified criteria.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `finder_name` | str | Yes | The Rest.li finder name. This will be added to the request query parameters. |

**Response:**

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
  }
  access_token=MY_ACCESS_TOKEN,
  version_string="202212"
)
ad_accounts = response.elements
total = response.paging.total
```

#### batch_finder *(resource_path, finder_name, finder_criteria, access_tokien, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li BATCH_FINDER request to find entities by multiple sets of criteria.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `finder_name` | str | Yes | The Rest.li batch finder name (the value of the "bq" query parameter). This will be added to the request query parameters. |
| `finder_criteria` | Tuple[str, List[Dict[str,Any]]] | The required batch finder criteria information. This is a tuple with the first value being the batch finder criteria parameter name. The second value is the list of finder param objects. The batch finder results are correspondingly ordered according to this list. The batch finder criteria will be encoded and added to the request query parameters. |

**Response:**

Returns a [BatchFinderResponse](#class-collectionresponse) object.

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

#### create *(resource_path, entity, access_token, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li CREATE request to create a new resource entity.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `entity` | Dict[str,Any] | Yes | A dictionary representation of the entity to create |

**Response:**

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

#### batch_create *(resource_path, entities, access_token, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li BATCH_CREATE request to create multiple entities in a single call.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `entities` | List[Dict[str,Any]] | Yes | A list of entities to create |

**Response:**

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

#### update *(resource_path, entity, access_token, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li UPDATE request to update an entity (overwriting the entity with the provided value).

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `entity` | Dict[str,Any] | Yes | The value of the updated entity. This will completely overwrite the entity. |

**Response:**

Returns a [UpdateResponse](#class-updateresponse) object.

**Example:**

```python
response = restli_client.update(
  resource_path="/adAccountUsers/{id}",
  path_keys={
    "id": {
      "account": 'urn:li:sponsoredAccount:123',
      "user": 'urn:li:person:foobar'
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

#### batch_update *(resource_path, ids, entities, access_token, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li BATCH_UPDATE request to update multiple entities in a single call.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `ids` | List[Union[str,int,Dict[str,Any]]] | Yes | The ids of the entities to update |
| `entities` | List[Dict[str,Any]] | Yes | The values to update the specified entities to. This should be the same order as the `ids` argument. |

**Response:**

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
batch_results_statuses = response.results.items()
```

#### *partial_update(resource_path, patch_set_object, access_token, path_keys=None, query_params=None, version_string=None)*

Makes a Rest.li PARTIAL_UPDATE request to update part of an entity. Directly specify the patch object to send in the request.

Note: While the Rest.li protocol supports very granular patch objects with setting and deletion of nested properties, most LinkedIn APIs only support partial update on the top-level fields of an entity.

**Parameters:**

The additional parameters besides the [base request parameters](#base-request-parameters) are:

| Parameter | Type | Required? | Description |
|---|---|---|---|
| `patch_set_object` | Dict[str,Any] | Yes | The value of the entity with only the modified fields present. This will be sent directly in the request body as `patch: { $set: patch_set_object }`. |

**Response:**

Returns a [UpdateResponse](#class-updateresponse) object.

**Example:**

```python
response = restli_client.partial_update(
  resource_path="/adAccounts",
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

#### *batch_partial_update(resource_path, ids, patch_set_objects, access_token, path_keys=None, query_params=None, version_string=None)*



### Response Classes

#### *class BaseRestliResponse()*

All Rest.li request methods of the API client return a response object subclassed from BaseRestliResponse, containing standard response data, along with the original, raw response object.

| Properties | Type | Description |
|---|---|---|
| `status_code` | int | Response status code |
| `url` | str | The final URL location of the response |
| `headers` | CaseInsensitiveDict | A case-insensitive dictionary of response headers |
| `response` | Response | The raw requests.Response object |

#### *class Paging()*

Paging metadata class

| Properties | Type | Description |
|---|---|---|
| start | int | The start index of returned results (zero-based index) |
| count | int | The number of results returned in the response |
| total | int | The total number of results available |

#### *class GetResponse()*

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `entity` | Union[Dict[str,Any], str, int, bool] | The representation (typically a dictionary) of the retrieved entity, decoded from the json-encoded response content |

#### *class BatchGetResponse()*

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `resultsMap` | Dict[str,Any] | A map of entities that were successfully retrieved, with the key being the encoded entity id, and the value being a dictionary representing the entity |
| `statusesMap` | Dict[str,int] | A map of entities and status code, with the key being the encoded entity id, and the value being the status code number value. |
| `errorsMap` | Dict[str,Any] | A map containing entities that could not be successfully fetched, with the key being the encoded entity id, and the value being the error response. |

#### *class CollectionResponse()*

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `elements` | List[Dict[str,Any]] | The list of entities returned in the response |
| `paging` | [Paging](#class-paging) | Optional paging metadata object |
| `metadata` | Any | Optional response metadata object |

#### *class BatchFinderResponse()*

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `results` | List[[BatchFinderResult](#class-batchfinderresult)] | The list of finder results, in the same order as the requested batch finder search criteria list |

#### *class BatchFinderResult()*

| Properties | Type | Description |
|---|---|---|
| `elements` | List[Dict[str,Any]] | The list of entities found for the corresponding finder criteria |
| `paging` | [Paging](#class-paging) | Optional paging metadata object |
| `metadata` | Any | Optional response metadata object |
| `error` | Any | Optional error details if finder call failed |
| `isError` | bool | Flag if this finder call experienced an error |

#### *class CreateResponse()*

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `entity_id` | str | The encoded entity id |
| `entity` | Dict[str,Any] | Optional created entity. Some APIs support returning the created entity to eliminate the need for a subsequent GET call. |

#### *class BatchCreateResponse()*

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `elements` | List[[BatchCreateResult](#class-batchcreateresult)] | The list of batch create results, corresponding to the order of the `entities` request parameter |

#### *class BatchCreateResult()*

| Properties | Type | Description |
|---|---|---|
| `status` | int | The status code of the individual create call |
| `id` | str | The id of the created entity |
| `error` | Any | Error details if the create call experienced an error |

#### *class UpdateResponse()*

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `entity` | Dict[str,Any] | Optional entity after the update. Some APIs support returning the updated entity to eliminate the need for a subsequent GET call. |

#### *class BatchUpdateResponse()*

Base class: [BaseRestliResponse](#class-baserestliresponse)

| Properties | Type | Description |
|---|---|---|
| `results` | Dict[str,[BatchUpdateResult](#class-batchupdateresult)] | The results map where the keys are the encoded entity ids, and the values are the individual update call results, which includes the status code. |

#### *class BatchUpdateResult()*

| Properties | Type | Description |
|---|---|---|
| `status` | int | The status code of the update call |