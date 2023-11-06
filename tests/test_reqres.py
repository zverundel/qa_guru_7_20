import jsonschema
import allure
import json
from curlify import to_curl
from utils import load_schema
from allure_commons.types import AttachmentType
from requests import sessions


def reqres_api(method, url, **kwargs):
    args = kwargs
    base_url = "https://reqres.in"
    new_url = base_url + url
    method = method.upper()
    with allure.step(f'Отправляем запрос {method} {url} {args if len(args) != 0 else ""} '):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            allure.attach(body=message.encode("utf8"), name="Curl", attachment_type=AttachmentType.TEXT,
                          extension='txt')
            allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"), name="Response Json",
                          attachment_type=AttachmentType.JSON, extension='json')
    return response


def test_get_single_user_status_not_ok():
    response = reqres_api('get', url='/api/users/23')
    assert (response.status_code == 404)


def test_get_list_status_ok():
    response = reqres_api('get', url='/api/unknown')
    assert (response.status_code == 200)


def test_param_get_delayed_response_status_ok():
    response = reqres_api('get', url='/api/users', params={"delay": 3})
    assert (response.status_code == 200)


def test_param_get_users_data_check():
    response = reqres_api('get', url='/api/users', params={"per_page": 2})
    assert(len(response.json()['data']) == 2)


def test_param_get_users_page_check():
    response = reqres_api('get', url='/api/users', params={"page":1})
    assert(response.json()['page']) == 1


def test_post_register_successful():
    schema = load_schema('post_register.json')
    response = reqres_api(
        'post', url='/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
    })
    assert response.status_code == 200
    assert response.json()['id'] == 4
    assert response.json()['token'] == "QpwL5tke4Pnpja7X4"
    jsonschema.validate(response.json(), schema)


def test_post_create_user_successfull():
    schema = load_schema('post_create_user.json')
    response = reqres_api(
        'post', url='/api/users',
        json = {
            "name": "morpheus",
            "job": "leader"
    })
    jsonschema.validate(response.json(), schema)
    assert response.status_code == 201
    assert response.json()['job'] == 'leader'


def test_put_update_user():
    schema = load_schema('put_update_user.json')
    response = reqres_api(
        'put', url='/api/users/2',
        json = {
            "name": "zverundel",
            "job": "QA"
    })
    jsonschema.validate(response.json(), schema)
    assert response.status_code == 200
    assert response.json()['name'] == 'zverundel'


def test_patch_update_user():
    schema = load_schema('patch_update_user.json')
    response = reqres_api(
        'patch', url='/api/users/2',
        json = {
            "name": "zverundel",
            "job": "QA"
    })
    jsonschema.validate(response.json(), schema)
    assert response.status_code == 200
    assert response.json()['job'] == 'QA'


def test_get_list_users():
    response = reqres_api(
        'get', url='/api/users',
        params={"page": 2}
    )
    assert response.status_code == 200
    assert response.json()["page"] == 2


def test_get_single_existing_user():
    response = reqres_api('get', url='/api/users/2')
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2


def test_get_user_not_found():
    response = reqres_api('get', url='/api/users/23')
    assert response.status_code == 404


def test_get_user_schema_validation():
    schema = load_schema('get_users.json')
    response = reqres_api('get', url='/api/users/2')
    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)