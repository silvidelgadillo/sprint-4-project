from locust import HttpUser, TaskSet, task, between

wait_time = between(1, 5)

class UserBehavior(TaskSet):
    @task(1)
    def index(self):
        self.client.get("http://localhost/")

    @task(3)
    def predict(self):
        self.client.get("http://localhost/")
        header  = {}
        data    = {}
        files   = [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
        self.client.post("http://localhost/predict", header = header, data = data, files = files)
        