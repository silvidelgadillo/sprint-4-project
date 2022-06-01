import  time
from    locust import HttpUser, TaskSet, task, between


class UserBehavior(HttpUser):
    wait_time = between(0.5,3.0)
    # task is something that we (the users) can run:
    @task(1)
    def index(self):
        self.client.get("http://localhost/")
 
    @task(3) # el 3 quiere decir que por cada vez que se ejecute el otro task 
    def predict(self):
        files = [('file',('dog.jpeg', open('dog.jpeg', 'rb'), 'image/jpeg'))] 
        headers = {}
        payload = {}
        self.client.post('http://localhost/predict', headers = headers, data = payload, files = files)

    # dont we need an on_start_method?
    

#class APIUser(HttpUser):
#    task_set = UserBehavior
#    min_wait = 1000
#    max_wait = 5000
#

    