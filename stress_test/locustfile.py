from locust import HttpUser, task, between


class UserBehavior(HttpUser):
    wait_time = between(0.5, 1)

    @task(1)
    def index(self):
        self.client.get("http://localhost/")

    @task(3)
    def predict(self):
        header = {}
        data = {}
        files = [
            ("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg")),
        ]
        self.client.post(
            "http://localhost/predict",
            headers=header,
            data=data,
            files=files,
        )
