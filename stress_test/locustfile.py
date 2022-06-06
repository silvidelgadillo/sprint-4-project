from email.mime import image
import time
from wsgiref import headers
from locust import TaskSet, task, HttpUser, between


class UserBehavior(TaskSet):
    # se define la estategia de interacción de los usuarios
    @task(1) # el 1 es que dará prio al index contra el predict de 1 a 3 veces
    def index(self):
        self.client.get("http://localhost/") #simple get

    @task(3)
    def predict(self): # le enviamos un archivo por metodo post 
    # Put your stress tests here
        files = [
            ("file",("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))
        ]
        header = {}
        payload = {}
        self.client.post(
            "http://localhost/predict/",
            headers=headers,
            data=payload,
            files=files,
        )
# antes que el usuario se conecta al endpoint tiene que esperar min wait, y el usuario  tiene que esperar max wait para un nuevo  request 
class APIUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1,10)
