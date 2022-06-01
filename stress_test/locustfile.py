from locust import HttpUser, TaskSet, task

class UserBehavior(HttpUser):

    @task(1)
    def index(self):
        self.client.get("http://localhost")

    @task(3)
    def predict(self):
        files = [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
        self.client.post("http://localhost/predict", files=files)


class APIUser(HttpUser):
    task_set = UserBehavior
