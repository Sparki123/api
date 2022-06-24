import pytest
import requests
import json

from Data.request_data import post_pet

base_url = "https://petstore.swagger.io/v2"


def test_get_pet_by_id_success() :
    path = "/pet/2"
    response = requests.get(url=base_url + path)
    response_json = json.loads(response.content)
    assert response.status_code == 200
    assert response_json["id"] == 2


def test_get_pet_by_id_failed():
    path = "/pet/122"
    response = requests.get(url=base_url + path)
    response_json = json.loads(response.content)
    assert response.status_code == 404
    assert response_json["type"] == 'error'
    assert response_json["message"] == 'Pet not found'


@pytest.mark.parametrize("status", ["sold", "pending", "available"])
def test_find_by_status(status):
    path = "/pet/findByStatus"
    response = requests.get(url=base_url + path, params={"status": status})
    response_json = json.loads(response.content)
    assert response.status_code == 200

    by_status = list(filter(lambda x: x["status"] == status, response_json))

    assert len(by_status) == len(response_json)


def test_find_by_status_negative():
    path = "/pet/findByStatus"
    response = requests.get(url=base_url + path, params={"status": "hello"})
    response_json = json.loads(response.content)
    assert response.status_code == 200
    assert len(response_json) == 0


def test_post_pet():
    path = "/pet"
    response = requests.post(url=base_url + path, json=post_pet)
    response_json = json.loads(response.content)
    assert response.status_code == 200
    assert response_json["id"]
    assert response_json["name"] == post_pet["name"]
    assert response_json["tags"] == post_pet["tags"]