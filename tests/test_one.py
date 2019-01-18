from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import requests as req
from jsonschema import validate
import json
import pytest


def test_facebook_on():
    capabilities = FirefoxOptions()
    desired_caps = capabilities.to_capabilities()
    desired_caps['enableVNC'] = True
    desired_caps['enableVideo'] = True

    driver = webdriver.Remote(
        command_executor="http://selenoid:4444/wd/hub",
        desired_capabilities=desired_caps)

    driver.get("https://www.facebook.com")
    driver.quit()


server_name = "https://reqres.in"


@pytest.mark.usefixtures('check_if_skipped')
def test_two():
    validate_get_json_request("/api/users?page=2", "test_two_schema")


def test_three(check_if_skipped):
    validate_post_json_request("/api/users", "test_three_schema", "test_three_data")


def test_four():
    validate_get_json_request("/api/users", "test_four_schema")


def test_five():
    validate_delete_request("/api/users/2")


def test_six():
    validate_get_request("/api/users/23", 404)


def test_seven():
    validate_get_json_request("/api/users", "test_seven_schema")


def test_eight():
    with open('resources/schemas/{}.json'.format("test_eight_schema"), 'r') as f:
        schema = json.load(f)
    validate([
        "life",
        "universe",
        "everything",
        8
    ], schema=schema)


def validate_get_json_request(api, schema_name):
    resp = req.get(server_name + api)
    # assert resp.status_code == 200
    with open('resources/schemas/{}.json'.format(schema_name), 'r') as f:
        schema = json.load(f)
    validate(resp.json(), schema=schema)


def validate_post_json_request(api, schema_name, post_data):
    with open('resources/test_data/{}.json'.format(post_data), 'r') as f:
        data = json.load(f)
    resp = req.post(server_name + api, data)
    assert resp.status_code == 201
    with open('resources/schemas/{}.json'.format(schema_name), 'r') as f:
        schema = json.load(f)
    validate(resp.json(), schema=schema)


def validate_delete_request(api):
    resp = req.delete(server_name + api)
    assert resp.status_code == 204
    assert resp.text == ""


def validate_get_request(api, status_code):
    resp = req.get(server_name + api)
    assert resp.status_code == status_code


@pytest.fixture()
def check_if_skipped(request):
    if request.node.name in ['test_two', 'test_three']:
        pytest.skip('This test skipped')
