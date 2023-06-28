import json
from linkedin_api.clients.restli.client import RestliClient
import pytest
import responses
from responses import matchers
from linkedin_api.common.constants import (
    NON_VERSIONED_BASE_URL,
    RESTLI_METHOD_TO_HTTP_METHOD_MAP,
    RESTLI_METHODS,
    VERSIONED_BASE_URL,
    HTTP_METHODS,
)
import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    from importlib_metadata import version

__version__ = version("linkedin-api-client")
ACCESS_TOKEN = "ABC123"
# 4000 characters string for testing query tunneling
LONG_STRING = "421yg4h2cqta89yov4x39ojnzinhhph9y36depvp4f249j5unznzl52jlgok1bxgwt965i58cyd3afdmlxuobebizt3ju7qwrwim9pl5omz4k5dwzkqy6cni9ys7o9w32fl0ysdp4lrwji8dcxi9eqlfb0ym6ykz4r93udolzrw9eci06w55ksqs0zw47jzfx1upe7bishjxdndgp5ya5y61z78ay83xhqakvac8h5b84398o82c93bpnzjrxoggn2xqx6qyrb2dw4s9008wlwcivskni2ztjvcaq0hk2odvrmrijwyzfbf443u0g4jmorgdrqye9ee9bberkx9n7u4m16ekrapvxgkcezhbborbaa5lzjz92c1vgr44cn7olhb7yt0nsrsoug7dzj2c6mv7cady17by66me0cdj9la10o2v1x5yls9tmdp4qlyxgu2o5f83sgezs1570imkzorp7xqjlzrm4zlhq8729ljoqrj5zb2400u5cgty81el9wos2t0p1ghlv0v7izzlskgdpe0dxglbvpdi53ys392p9dp6lta8ms286r0pqvqgjepzzb5s4x5bq5mga1o1iwx2l4qn6oi3wqvr3octwb37s90h3ikw0b1imjko9i1z8b2bn05ud6df0nmkftsx2g3n32zdk8o9rgv428ifbc2n7nspyykljj4f8fc7xyhbx5aq3bwz6bca3yp8jebaxo92dbbo393cm41mjotdd2wov7agiydl6kv3gk2sa93p8j31bbne6t96gg5zamemcejj468hw1qbed4oiz5xkt4riuqsqawhb7uqgn4fa6ntonymyycgpq0zsuu66cxw011xp3sxehzgkesytivtx08pa0dtbv25xqx78ok9gc2fvockdnzkzpz46kchex2qyn742wty5d1ljsi7ffau5zpi62ntxid5px6zs2yuprc7rhq9s9j4plw0mqs21grdjmhmzgsn2ro640ezuoh0421yg4h2cqta89yov4x39ojnzinhhph9y36depvp4f249j5unznzl52jlgok1bxgwt965i58cyd3afdmlxuobebizt3ju7qwrwim9pl5omz4k5dwzkqy6cni9ys7o9w32fl0ysdp4lrwji8dcxi9eqlfb0ym6ykz4r93udolzrw9eci06w55ksqs0zw47jzfx1upe7bishjxdndgp5ya5y61z78ay83xhqakvac8h5b84398o82c93bpnzjrxoggn2xqx6qyrb2dw4s9008wlwcivskni2ztjvcaq0hk2odvrmrijwyzfbf443u0g4jmorgdrqye9ee9bberkx9n7u4m16ekrapvxgkcezhbborbaa5lzjz92c1vgr44cn7olhb7yt0nsrsoug7dzj2c6mv7cady17by66me0cdj9la10o2v1x5yls9tmdp4qlyxgu2o5f83sgezs1570imkzorp7xqjlzrm4zlhq8729ljoqrj5zb2400u5cgty81el9wos2t0p1ghlv0v7izzlskgdpe0dxglbvpdi53ys392p9dp6lta8ms286r0pqvqgjepzzb5s4x5bq5mga1o1iwx2l4qn6oi3wqvr3octwb37s90h3ikw0b1imjko9i1z8b2bn05ud6df0nmkftsx2g3n32zdk8o9rgv428ifbc2n7nspyykljj4f8fc7xyhbx5aq3bwz6bca3yp8jebaxo92dbbo393cm41mjotdd2wov7agiydl6kv3gk2sa93p8j31bbne6t96gg5zamemcejj468hw1qbed4oiz5xkt4riuqsqawhb7uqgn4fa6ntonymyycgpq0zsuu66cxw011xp3sxehzgkesytivtx08pa0dtbv25xqx78ok9gc2fvockdnzkzpz46kchex2qyn742wty5d1ljsi7ffau5zpi62ntxid5px6zs2yuprc7rhq9s9j4plw0mqs21grdjmhmzgsn2ro640ezuoh0421yg4h2cqta89yov4x39ojnzinhhph9y36depvp4f249j5unznzl52jlgok1bxgwt965i58cyd3afdmlxuobebizt3ju7qwrwim9pl5omz4k5dwzkqy6cni9ys7o9w32fl0ysdp4lrwji8dcxi9eqlfb0ym6ykz4r93udolzrw9eci06w55ksqs0zw47jzfx1upe7bishjxdndgp5ya5y61z78ay83xhqakvac8h5b84398o82c93bpnzjrxoggn2xqx6qyrb2dw4s9008wlwcivskni2ztjvcaq0hk2odvrmrijwyzfbf443u0g4jmorgdrqye9ee9bberkx9n7u4m16ekrapvxgkcezhbborbaa5lzjz92c1vgr44cn7olhb7yt0nsrsoug7dzj2c6mv7cady17by66me0cdj9la10o2v1x5yls9tmdp4qlyxgu2o5f83sgezs1570imkzorp7xqjlzrm4zlhq8729ljoqrj5zb2400u5cgty81el9wos2t0p1ghlv0v7izzlskgdpe0dxglbvpdi53ys392p9dp6lta8ms286r0pqvqgjepzzb5s4x5bq5mga1o1iwx2l4qn6oi3wqvr3octwb37s90h3ikw0b1imjko9i1z8b2bn05ud6df0nmkftsx2g3n32zdk8o9rgv428ifbc2n7nspyykljj4f8fc7xyhbx5aq3bwz6bca3yp8jebaxo92dbbo393cm41mjotdd2wov7agiydl6kv3gk2sa93p8j31bbne6t96gg5zamemcejj468hw1qbed4oiz5xkt4riuqsqawhb7uqgn4fa6ntonymyycgpq0zsuu66cxw011xp3sxehzgkesytivtx08pa0dtbv25xqx78ok9gc2fvockdnzkzpz46kchex2qyn742wty5d1ljsi7ffau5zpi62ntxid5px6zs2yuprc7rhq9s9j4plw0mqs21grdjmhmzgsn2ro640ezuoh0421yg4h2cqta89yov4x39ojnzinhhph9y36depvp4f249j5unznzl52jlgok1bxgwt965i58cyd3afdmlxuobebizt3ju7qwrwim9pl5omz4k5dwzkqy6cni9ys7o9w32fl0ysdp4lrwji8dcxi9eqlfb0ym6ykz4r93udolzrw9eci06w55ksqs0zw47jzfx1upe7bishjxdndgp5ya5y61z78ay83xhqakvac8h5b84398o82c93bpnzjrxoggn2xqx6qyrb2dw4s9008wlwcivskni2ztjvcaq0hk2odvrmrijwyzfbf443u0g4jmorgdrqye9ee9bberkx9n7u4m16ekrapvxgkcezhbborbaa5lzjz92c1vgr44cn7olhb7yt0nsrsoug7dzj2c6mv7cady17by66me0cdj9la10o2v1x5yls9tmdp4qlyxgu2o5f83sgezs1570imkzorp7xqjlzrm4zlhq8729ljoqrj5zb2400u5cgty81el9wos2t0p1ghlv0v7izzlskgdpe0dxglbvpdi53ys392p9dp6lta8ms286r0pqvqgjepzzb5s4x5bq5mga1o1iwx2l4qn6oi3wqvr3octwb37s90h3ikw0b1imjko9i1z8b2bn05ud6df0nmkftsx2g3n32zdk8o9rgv428ifbc2n7nspyykljj4f8fc7xyhbx5aq3bwz6bca3yp8jebaxo92dbbo393cm41mjotdd2wov7agiydl6kv3gk2sa93p8j31bbne6t96gg5zamemcejj468hw1qbed4oiz5xkt4riuqsqawhb7uqgn4fa6ntonymyycgpq0zsuu66cxw011xp3sxehzgkesytivtx08pa0dtbv25xqx78ok9gc2fvockdnzkzpz46kchex2qyn742wty5d1ljsi7ffau5zpi62ntxid5px6zs2yuprc7rhq9s9j4plw0mqs21grdjmhmzgsn2ro640ezuoh0"


"""
Tests for basic functionality of the RestliClient methods, providing
the input request options and method type and expected response.
"""


@pytest.mark.parametrize(
    "restli_method,request_args,input_response,expected_values",
    [
        #
        # GET Method
        #
        (
            # Get request for a non-versioned collection resources, checking basic headers
            RESTLI_METHODS.GET,
            {
                # request_args
                "resource_path": "/adAccounts/{id}",
                "path_keys": {"id": 123},
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {"name": "TestAdAccount"},
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/adAccounts/123",
                "checked_headers": {
                    "Connection": "Keep-Alive",
                    "Authorization": "Bearer ABC123",
                    "X-RestLi-Protocol-Version": "2.0.0",
                    "Content-Type": "application/json",
                    "X-RestLi-Method": RESTLI_METHODS.GET.value,
                    "User-Agent": f"linkedin-api-python-client/{__version__}",
                },
                "response_properties": {"entity": {"name": "TestAdAccount"}},
            },
        ),
        (
            # Get request with basic query params, check basic headers
            RESTLI_METHODS.GET,
            {
                # request_args
                "resource_path": "/adAccounts/{id}",
                "path_keys": {"id": 123},
                "query_params": {"param1": "foobar", "param2": 123},
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {"name": "TestAdAccount"},
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/adAccounts/123?param1=foobar&param2=123",
            },
        ),
        (
            # Get request for a simple resource
            RESTLI_METHODS.GET,
            {
                # request_args
                "resource_path": "/me",
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {"name": "Me"},
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/me",
            },
        ),
        (
            # Get request for a versioned collection resource
            RESTLI_METHODS.GET,
            {
                # request_args
                "resource_path": "/me",
                "access_token": ACCESS_TOKEN,
                "version_string": "202212",
            },
            {
                # input_response
                "json": {"name": "Me"},
                "status": 200,
            },
            {
                # expected_values
                "base_url": VERSIONED_BASE_URL,
                "path": "/me",
                "checked_headers": {"LinkedIn-Version": "202212"},
            },
        ),
        (
            # Get request with field projections
            RESTLI_METHODS.GET,
            {
                # request_args
                "resource_path": "/me",
                "access_token": ACCESS_TOKEN,
                "query_params": {"param1": [1, 2, 3], "fields": "id,firstName"},
            },
            {
                # input_response
                "json": {"name": "Me"},
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/me?param1=List(1,2,3)&fields=id,firstName",
            },
        ),
        #
        # BATCH_GET Method
        #
        (
            # Batch get request for a non-versioned collection resource
            RESTLI_METHODS.BATCH_GET,
            {
                # request_args
                "resource_path": "/testResource",
                "ids": [123, 456, 789],
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {
                    "results": {
                        "123": {"name": "A"},
                        "456": {"name": "B"},
                        "789": {"name": "C"},
                    }
                },
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource?ids=List(123,456,789)",
                "response_properties": {
                    "results": {
                        "123": {"name": "A"},
                        "456": {"name": "B"},
                        "789": {"name": "C"},
                    },
                    "statuses": None,
                    "errors": None,
                },
            },
        ),
        (
            # Batch get request for a non-versioned collection resource
            RESTLI_METHODS.BATCH_GET,
            {
                # request_args
                "resource_path": "/testResource",
                "ids": [
                    {"member": "urn:li:person:123", "account": "urn:li:account:234"},
                    {"member": "urn:li:person:234", "account": "urn:li:account:345"},
                    {"member": "urn:li:person:345", "account": "urn:li:account:456"},
                ],
                "query_params": {
                    "param1": "foobar",
                    "param2": {"prop1": "abc", "prop2": "def"},
                },
                "access_token": ACCESS_TOKEN,
                "version_string": "202210",
            },
            {
                # input_response
                "json": {
                    "results": {
                        "(member:urn%3Ali%3Aperson%3A123,account:urn%3Ali%3Aaccount%3A234)": {
                            "name": "A"
                        },
                        "(member:urn%3Ali%3Aperson%3A234,account:urn%3Ali%3Aaccount%3A345)": {
                            "name": "B"
                        },
                        "(member:urn%3Ali%3Aperson%3A345,account:urn%3Ali%3Aaccount%3A456)": {
                            "name": "C"
                        },
                    }
                },
                "status": 200,
            },
            {
                # expected_values
                "base_url": VERSIONED_BASE_URL,
                "path": "/testResource?ids=List((account:urn%3Ali%3Aaccount%3A234,member:urn%3Ali%3Aperson%3A123),(account:urn%3Ali%3Aaccount%3A345,member:urn%3Ali%3Aperson%3A234),(account:urn%3Ali%3Aaccount%3A456,member:urn%3Ali%3Aperson%3A345))&param1=foobar&param2=(prop1:abc,prop2:def)",
                "response_properties": {
                    "results": {
                        "(member:urn%3Ali%3Aperson%3A123,account:urn%3Ali%3Aaccount%3A234)": {
                            "name": "A"
                        },
                        "(member:urn%3Ali%3Aperson%3A234,account:urn%3Ali%3Aaccount%3A345)": {
                            "name": "B"
                        },
                        "(member:urn%3Ali%3Aperson%3A345,account:urn%3Ali%3Aaccount%3A456)": {
                            "name": "C"
                        },
                    },
                    "statuses": None,
                    "errors": None,
                },
            },
        ),
        (
            # Batch get request with query tunneling
            RESTLI_METHODS.BATCH_GET,
            {
                # request_args
                "resource_path": "/testResource",
                "ids": [123, 456],
                "query_params": {"longParam": LONG_STRING},
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {"results": {"123": {"name": "A"}, "456": {"name": "B"}}},
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource",
                "request_override_method": HTTP_METHODS.POST.value,
                "request_body": {
                    "type": "urlencoded",
                    "value": {"ids": "List(123,456)", "longParam": LONG_STRING},
                },
                "response_properties": {
                    "results": {"123": {"name": "A"}, "456": {"name": "B"}},
                    "statuses": None,
                    "errors": None,
                },
                "checked_headers": {
                    "X-HTTP-Method-Override": "GET",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            },
        ),
        #
        # GET_ALL Method
        #
        (
            # Get all request for a non-versioned collection resource
            RESTLI_METHODS.GET_ALL,
            {
                # request_args
                "resource_path": "/testResource",
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {
                    "elements": [{"name": "A"}, {"name": "B"}],
                    "paging": {"start": 0, "count": 2, "total": 10},
                },
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource",
                "checked_headers": {"X-RestLi-Method": RESTLI_METHODS.GET_ALL.value},
                "response_properties": {
                    "elements": [{"name": "A"}, {"name": "B"}],
                    "paging": {"start": 0, "count": 2, "total": 10},
                },
            },
        ),
        #
        # FINDER Method
        #
        (
            # Finder request on a non-versioned collection resource
            RESTLI_METHODS.FINDER,
            {
                # request_args
                "resource_path": "/testResource",
                "finder_name": "search",
                "query_params": {
                    "search": {
                        "ids": {"values": ["urn:li:entity:123", "urn:li:entity:456"]}
                    }
                },
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {
                    "elements": [{"name": "A"}, {"name": "B"}],
                    "paging": {"start": 0, "count": 2, "total": 10},
                },
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource?q=search&search=(ids:(values:List(urn%3Ali%3Aentity%3A123,urn%3Ali%3Aentity%3A456)))",
                "checked_headers": {"X-RestLi-Method": RESTLI_METHODS.FINDER.value},
                "response_properties": {
                    "elements": [{"name": "A"}, {"name": "B"}],
                    "paging": {"start": 0, "count": 2, "total": 10},
                },
            },
        ),
        #
        # BATCH_FINDER Method
        #
        (
            # Batch finder request on a non-versioned collection resource
            RESTLI_METHODS.BATCH_FINDER,
            {
                # request_args
                "resource_path": "/testResource",
                "finder_name": "authActions",
                "finder_criteria": (
                    "authActionsCriteria",
                    [
                        {"OrgRoleAuthAction": {"actionType": "ADMIN_READ"}},
                        {
                            "OrgContentAuthAction": {
                                "actionType": "ORGANIC_SHARE_DELETE"
                            }
                        },
                    ],
                ),
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {"elements": [{"elements": []}, {"elements": []}]},
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource?authActionsCriteria=List((OrgRoleAuthAction:(actionType:ADMIN_READ)),(OrgContentAuthAction:(actionType:ORGANIC_SHARE_DELETE)))&bq=authActions",
                "checked_headers": {
                    "X-RestLi-Method": RESTLI_METHODS.BATCH_FINDER.value
                },
                "response_properties": {
                    "results": [
                        {
                            "elements": [],
                            "paging": None,
                            "metadata": None,
                            "error": None,
                            "isError": False,
                        },
                        {
                            "elements": [],
                            "paging": None,
                            "metadata": None,
                            "error": None,
                            "isError": False,
                        },
                    ]
                },
            },
        ),
        #
        # CREATE Method
        #
        (
            # Create request on a non-versioned collection resource, with no entity returned
            RESTLI_METHODS.CREATE,
            {
                # request_args
                "resource_path": "/testResource",
                "entity": {"name": "TestApp1"},
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": None,
                "status": 201,
                "headers": {"x-restli-id": "123"},
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource",
                "checked_headers": {"X-RestLi-Method": RESTLI_METHODS.CREATE.value},
                "response_properties": {
                    "entity_id": "123",
                    "decoded_entity_id": "123",
                    "entity": None,
                },
            },
        ),
        (
            # Create request on a non-versioned collection resource, with complex entity id
            RESTLI_METHODS.CREATE,
            {
                # request_args
                "resource_path": "/testResource",
                "entity": {"name": "TestApp1"},
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": None,
                "status": 201,
                "headers": {"x-restli-id": "urn%3Ali%3Aapp%3A123?"},
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource",
                "checked_headers": {"X-RestLi-Method": RESTLI_METHODS.CREATE.value},
                "response_properties": {
                    "entity_id": "urn%3Ali%3Aapp%3A123?",
                    "decoded_entity_id": "urn:li:app:123?",
                    "entity": None,
                },
            },
        ),
        (
            # Create request on a non-versioned collection resource, with entity returned
            RESTLI_METHODS.CREATE,
            {
                # request_args
                "resource_path": "/testResource",
                "entity": {"name": "TestApp1"},
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {"name": "TestApp1", "reference": "foobar123"},
                "status": 201,
                "headers": {"x-restli-id": "123"},
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource",
                "checked_headers": {"X-RestLi-Method": RESTLI_METHODS.CREATE.value},
                "response_properties": {
                    "entity_id": "123",
                    "decoded_entity_id": "123",
                    "entity": {"name": "TestApp1", "reference": "foobar123"},
                },
            },
        ),
        #
        # BATCH_CREATE Method
        #
        (
            # Create request on a non-versioned collection resource, with entity returned
            RESTLI_METHODS.BATCH_CREATE,
            {
                # request_args
                "resource_path": "/adCampaignGroups",
                "entities": [
                    {"account": "urn:li:sponsoredAccount:111", "name": "Test1"},
                    {"account": "urn:li:sponsoredAccount:222", "name": "Test2"},
                ],
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {
                    "elements": [
                        {"status": 201, "id": 123},
                        {"status": 400, "error": "Unknown account"},
                    ]
                },
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/adCampaignGroups",
                "checked_headers": {
                    "X-RestLi-Method": RESTLI_METHODS.BATCH_CREATE.value
                },
                "response_properties": {
                    "elements": [
                        {"status": 201, "id": 123, "error": None},
                        {"status": 400, "id": None, "error": "Unknown account"},
                    ]
                },
            },
        ),
        #
        # PARTIAL_UPDATE Method
        #
        (
            # Partial update request on a non-versioned collection resource
            RESTLI_METHODS.PARTIAL_UPDATE,
            {
                # request_args
                "resource_path": "/testResource/{id}",
                "path_keys": {"id": 123},
                "patch_set_object": {"description": "modified description"},
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": None,
                "status": 201,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource/123",
                "checked_headers": {
                    "X-RestLi-Method": RESTLI_METHODS.PARTIAL_UPDATE.value
                },
                "request_body": {
                    "type": "json",
                    "value": {
                        "patch": {"$set": {"description": "modified description"}}
                    },
                },
            },
        ),
        #
        # BATCH_PARTIAL_UPDATE Method
        #
        (
            # Batch partial update request on a non-versioned collection resource
            RESTLI_METHODS.BATCH_PARTIAL_UPDATE,
            {
                # request_args
                "resource_path": "/testResource",
                "ids": ["urn:li:person:123", "urn:li:person:456"],
                "patch_set_objects": [
                    {"name": "Steven", "description": "foobar"},
                    {"prop1": 123},
                ],
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {
                    "results": {
                        "urn%3Ali%3Aperson%3A123": {"status": 204},
                        "urn%3Ali%3Aperson%3A456": {"status": 204},
                    }
                },
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource?ids=List(urn%3Ali%3Aperson%3A123,urn%3Ali%3Aperson%3A456)",
                "checked_headers": {
                    "X-RestLi-Method": RESTLI_METHODS.BATCH_PARTIAL_UPDATE.value
                },
                "request_body": {
                    "type": "json",
                    "value": {
                        "entities": {
                            "urn%3Ali%3Aperson%3A123": {
                                "patch": {
                                    "$set": {"name": "Steven", "description": "foobar"}
                                }
                            },
                            "urn%3Ali%3Aperson%3A456": {
                                "patch": {"$set": {"prop1": 123}}
                            },
                        }
                    },
                },
                "response_properties": {
                    "results": {
                        "urn%3Ali%3Aperson%3A123": {"status": 204},
                        "urn%3Ali%3Aperson%3A456": {"status": 204},
                    }
                },
            },
        ),
        #
        # UPDATE Method
        #
        (
            # Update a versioned, association resource
            RESTLI_METHODS.UPDATE,
            {
                # request_args
                "resource_path": "/testResource/{key}",
                "path_keys": {
                    "key": {
                        "application": "urn:li:developerApplication:123",
                        "member": "urn:li:member:456",
                    }
                },
                "entity": {"name": "Steven", "description": "foobar"},
                "version_string": "202210",
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": None,
                "status": 204,
            },
            {
                # expected_values
                "base_url": VERSIONED_BASE_URL,
                "path": "/testResource/(application:urn%3Ali%3AdeveloperApplication%3A123,member:urn%3Ali%3Amember%3A456)",
                "checked_headers": {
                    "LinkedIn-Version": "202210",
                    "X-RestLi-Method": RESTLI_METHODS.UPDATE.value,
                },
                "request_body": {
                    "type": "json",
                    "value": {"name": "Steven", "description": "foobar"},
                },
            },
        ),
        #
        # BATCH_UPDATE Method
        #
        (
            # Batch update on versioned resource
            RESTLI_METHODS.BATCH_UPDATE,
            {
                # request_args
                "resource_path": "/testResource",
                "ids": [
                    {
                        "application": "urn:li:developerApplication:123",
                        "member": "urn:li:member:321",
                    },
                    {
                        "application": "urn:li:developerApplication:789",
                        "member": "urn:li:member:987",
                    },
                ],
                "entities": [{"name": "foobar"}, {"name": "barbaz"}],
                "version_string": "202303",
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {
                    "results": {
                        "(application:urn%3Ali%3AdeveloperApplication%3A123,member:urn%3Ali%3Amember%3A321)": {
                            "status": 204
                        },
                        "(application:urn%3Ali%3AdeveloperApplication%3A789,member:urn%3Ali%3Amember%3A987)": {
                            "status": 204
                        },
                    }
                },
                "status": 200,
            },
            {
                # expected_values
                "base_url": VERSIONED_BASE_URL,
                "path": "/testResource?ids=List((application:urn%3Ali%3AdeveloperApplication%3A123,member:urn%3Ali%3Amember%3A321),(application:urn%3Ali%3AdeveloperApplication%3A789,member:urn%3Ali%3Amember%3A987))",
                "checked_headers": {
                    "LinkedIn-Version": "202303",
                    "X-RestLi-Method": RESTLI_METHODS.BATCH_UPDATE.value,
                },
                "request_body": {
                    "type": "json",
                    "value": {
                        "entities": {
                            "(application:urn%3Ali%3AdeveloperApplication%3A123,member:urn%3Ali%3Amember%3A321)": {
                                "name": "foobar"
                            },
                            "(application:urn%3Ali%3AdeveloperApplication%3A789,member:urn%3Ali%3Amember%3A987)": {
                                "name": "barbaz"
                            },
                        }
                    },
                },
                "response_properties": {
                    "results": {
                        "(application:urn%3Ali%3AdeveloperApplication%3A123,member:urn%3Ali%3Amember%3A321)": {
                            "status": 204
                        },
                        "(application:urn%3Ali%3AdeveloperApplication%3A789,member:urn%3Ali%3Amember%3A987)": {
                            "status": 204
                        },
                    }
                },
            },
        ),
        #
        # DELETE Method
        #
        (
            # Delete on a non-versioned collection resource
            RESTLI_METHODS.DELETE,
            {
                # request_args
                "resource_path": "/testResource/{id}",
                "path_keys": {"id": 123},
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": None,
                "status": 204,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource/123",
                "checked_headers": {"X-RestLi-Method": RESTLI_METHODS.DELETE.value},
                "response_properties": {"status_code": 204},
            },
        ),
        #
        # BATCH_DELETE Method
        #
        (
            # Batch delete on a non-versioned collection resource
            RESTLI_METHODS.BATCH_DELETE,
            {
                # request_args
                "resource_path": "/testResource",
                "ids": ["urn:li:member:123", "urn:li:member:456"],
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {
                    "results": {
                        "urn%3Ali%3Amember%3A123": {"status": 204},
                        "urn%3Ali%3Amember%3A456": {"status": 204},
                    }
                },
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource?ids=List(urn%3Ali%3Amember%3A123,urn%3Ali%3Amember%3A456)",
                "checked_headers": {
                    "X-RestLi-Method": RESTLI_METHODS.BATCH_DELETE.value
                },
                "response_properties": {
                    "results": {
                        "urn%3Ali%3Amember%3A123": {"status": 204},
                        "urn%3Ali%3Amember%3A456": {"status": 204},
                    }
                },
            },
        ),
        #
        # ACTION Method
        #
        (
            # Action on a non-versioned collection resource
            RESTLI_METHODS.ACTION,
            {
                # request_args
                "resource_path": "/testResource",
                "action_name": "doSomething",
                "action_params": {"actionParam1": 123, "actionParam2": "foobar"},
                "access_token": ACCESS_TOKEN,
            },
            {
                # input_response
                "json": {"value": {"result": "I did it!"}},
                "status": 200,
            },
            {
                # expected_values
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/testResource?action=doSomething",
                "checked_headers": {"X-RestLi-Method": RESTLI_METHODS.ACTION.value},
                "request_body": {
                    "type": "json",
                    "value": {"actionParam1": 123, "actionParam2": "foobar"},
                },
                "response_properties": {
                    "status_code": 200,
                    "value": {"result": "I did it!"},
                },
            },
        ),
    ],
)
@responses.activate
def test_restliclient(
    restli_method: RESTLI_METHODS, request_args, input_response, expected_values
):
    restli_client = RestliClient()

    # Create the expected url based on restli method and path
    # The http method is derived from the request_override_method (specified in the case of query tunneling)
    # or the mapping of Restli method to HTTP method
    request_override_method = expected_values.get("request_override_method", None)
    http_method = (
        request_override_method.lower()
        if request_override_method is not None
        else RESTLI_METHOD_TO_HTTP_METHOD_MAP[restli_method.value.upper()].lower()
    )
    expected_full_url = expected_values["base_url"] + expected_values["path"]
    expected_url_no_params = expected_full_url.split("?")[0]

    # Setup header matchers if needed
    checked_headers_dict = expected_values.get("checked_headers", None)
    request_matchers = (
        [matchers.header_matcher({k: v}) for (k, v) in checked_headers_dict.items()]
        if checked_headers_dict
        else []
    )

    # Setup request body matchers if needed
    request_body = expected_values.get("request_body", None)
    if request_body:
        request_body_content_type = request_body.get("type")
        request_body_value = request_body.get("value")
        if request_body_content_type == "urlencoded":
            request_matchers.append(
                matchers.urlencoded_params_matcher(request_body_value)
            )
        elif request_body_content_type == "json":
            request_matchers.append(matchers.json_params_matcher(request_body_value))

    requests_stub_args = {
        "url": expected_url_no_params,
        "json": input_response["json"],
        "status": input_response["status"],
        "headers": input_response.get("headers", {}),
    }

    if request_matchers:
        # Require matching any provided headers
        requests_stub_args.update({"match": request_matchers})

    # Mock the requests method according to expected_values
    getattr(responses, http_method)(**requests_stub_args)

    # Run RestliClient method with provided request args
    response = getattr(restli_client, restli_method.value.lower())(**request_args)

    # Verify expected request made
    print(f"Actual request URL: {response.url}")
    responses.assert_call_count(expected_full_url, 1)
    assert response.status_code == input_response["status"]

    # Verify the provided response_properties.
    # This will check the desired subset of the properties on the actual response.
    response_properties = expected_values.get("response_properties", None)
    if response_properties:
        for key in response_properties.keys():
            # Convert response attribute to a dictionary for comparison
            actual_response_property = to_dict(getattr(response, key))
            assert actual_response_property == response_properties.get(key)


def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))
