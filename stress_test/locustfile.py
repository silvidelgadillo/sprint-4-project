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
        # le paso una lista con una tupla --> es una lista de un elemento y ese elemento es una tupla.
        # a este endpoint se le pasa un archivo (el que euqeremos predecir) por eso ademas del url le paso file.
        files = [('file',('dog.jpeg', open('dog.jpeg', 'rb'), 'image/jpeg'))] 
        headers = {}
        payload = {}
        self.client.post('http://localhost/predict', headers = headers, data = payload, files = files)



    