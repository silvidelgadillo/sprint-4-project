import time
from locust import HttpUser, task, between


class UserBeh(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def index(self):
        self.client.get("http://localhost/")

    @task(3)
    def predict(self):
        self.client.get("http://localhost/")
        files   = ["file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg")]
        self.client.post("http://localhost/", header = {}, data = {}, files = files)