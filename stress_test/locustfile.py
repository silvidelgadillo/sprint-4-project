# import time
# from locust import HttpUser, TaskSet, task, between

# wait_time = between(1, 5)


# class UserBehavior(TaskSet):
#     @task(1)
#     def index(self):
#         self.client.get("http://localhost/")

#     @task(3)
#     def predict(self):
#         self.client.get("http://localhost/")
#         files   = [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
#         self.client.post("http://localhost/predict", header = {}, data = {}, files = files)
# class APIUser(HttpUser):
#     tasks = [UserBehavior]
from locust import HttpUser, task


class UserBehavior(HttpUser):
    max_wait = 5000
    min_wait = 1000

    @task(1)
    def index(self):
        self.client.get('http://localhost/')
    

    @task(2)
    def predict(self):
        file = [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
        self.client.post('http://localhost/predict', headers = {}, data = {}, files = file)