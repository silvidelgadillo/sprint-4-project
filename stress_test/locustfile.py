from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):

    @task(1)
    def test_index(self):
        self.client.get("http://localhost/")

    @task(3)
    def test_predict(self):
        file = [
            ("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))
        ]
        headers = {}
        payload = {}
        self.client.post("http://localhost/predict", files=file, headers=headers, data=payload)
class APIUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 5*1000
