import time
from stress_test.locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    # task is something that we (the users) can run:
    @task
    def index(self):
        self.client.get("http://0.0.0.0/")
 
    @task(3) # el 3 quiere decir que por cada vez que se ejecute el otro task 
    def predict(self):
        files = ['file',('dog.jpeg', open('dog.jpeg', 'rb'), 'image/jpeg')]
        headers = {}
        payload = {}
        self.client.post('http://0.0.0.0/predict', headers = headers, data = payload, files = files)

    # dont we need an on_start_method?
    

class APIUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000


    