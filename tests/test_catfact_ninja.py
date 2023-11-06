import jsonschema
import allure
import json
from curlify import to_curl
from utils import load_schema
from allure_commons.types import AttachmentType
from requests import sessions


def reqres_api(method, url, **kwargs):
    args = kwargs
    base_url = "https://catfact.ninja"
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


def test_get_breeds():
    page = 1
    response = reqres_api(
        'get',
        url='/breeds',
        params={"page": page}
    )
    assert response.status_code == 200
    assert response.json()["current_page"] == 1


def test_breeds_schema_validation():
    schema = load_schema('get_breeds.json')
    response = reqres_api(
        'get',
        url='/breeds'
    )
    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_get_random_fact():
    schema = load_schema('get_randon_fact.json')
    response = reqres_api(
        'get',
        url='/fact'
    )
    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)