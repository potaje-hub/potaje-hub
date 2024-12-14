from locust import HttpUser, task, between


class ExploreUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def view_explore(self):
        with self.client.get("/explore", catch_response=True) as response:
            if response.status_code == 200:
                print("Dataset list loaded successfully.")
            else:
                print(f"Error loading datasests list: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def filter_datasets_by_number_of_models(self):
        json = {

            "csrf_token": "IjEzMDgyNDU5OGQ3ZDUzMTRlYjgyMDkwYjhiZjM0ZWNjMjYyNjNlMDYi.Z118qQ.N9ojQBVDUmUfLOW0pqYBacOMk5o",
            "number_of_features": "",
            "number_of_models": "5",
            "publication_type": "any",
            "query": "",
            "sorting": "newest"

        }
        with self.client.post("/explore", json=json, catch_response=True) as response:
            if response.status_code == 200:
                print("Datasets filtered successfully.")
            else:
                print(f"Error filtering datasets: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(3)
    def filter_datasets_by_number_of_features(self):
        json = {

            "csrf_token": "IjEzMDgyNDU5OGQ3ZDUzMTRlYjgyMDkwYjhiZjM0ZWNjMjYyNjNlMDYi.Z118qQ.N9ojQBVDUmUfLOW0pqYBacOMk5o",
            "number_of_features": "50",
            "number_of_models": "",
            "publication_type": "any",
            "query": "",
            "sorting": "newest"

        }
        with self.client.post("/explore", json=json, catch_response=True) as response:
            if response.status_code == 200:
                print("Datasets filtered successfully.")
            else:
                print(f"Error filtering datasets: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")
