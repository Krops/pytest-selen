from locust import HttpLocust, TaskSet, task
from jsonschema import validate
import json


class MyTaskSet(TaskSet):
    server_name = "https://reqres.in"

    @task(2)
    def test_two(self):
        self.validate_get_json_request("/api/users?page=2", "test_two_schema")

    @task(2)
    def test_three(self):
        self.validate_post_json_request("/api/users", "test_three_schema", "test_three_data")

    @task(2)
    def test_four(self):
        self.validate_get_json_request("/api/users", "test_four_schema")

    @task(1)
    def test_five(self):
        self.validate_delete_request("/api/users/2")

    @task(1)
    def test_seven(self):
        self.validate_get_json_request("/api/users", "test_seven_schema")

    def validate_get_json_request(self, api, schema_name):
        resp = self.client.get(self.server_name + api)
        with open('resources/schemas/{}.json'.format(schema_name), 'r') as f:
            schema = json.load(f)
        validate(resp.json(), schema=schema)

    def validate_post_json_request(self, api, schema_name, post_data):
        with open('resources/test_data/{}.json'.format(post_data), 'r') as f:
            data = json.load(f)
        resp = self.client.post(self.server_name + api, data)
        assert resp.status_code == 201
        with open('resources/schemas/{}.json'.format(schema_name), 'r') as f:
            schema = json.load(f)
        validate(resp.json(), schema=schema)

    def validate_delete_request(self, api):
        resp = self.client.delete(self.server_name + api)
        assert resp.status_code == 204
        assert resp.text == ""

    def validate_get_request(self, api, status_code):
        resp = self.client.get(self.server_name + api)
        assert resp.status_code == status_code


class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 5000
    max_wait = 15000
