from locust import task, between, HttpUser


class UserBehavior(HttpUser):
    # Put your stress tests here
    # TODO
    wait_time = between(1, 5)

    @task(10)
    def index(self):
        self.client.get("http://127.0.0.1/")

    @task(30)
    def predict(self):
        with open("dog.jpeg", "rb") as image:
            self.client.post("http://127.0.0.1/predict", files={"file": image})
