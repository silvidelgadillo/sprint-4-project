from locust import HttpUser, between, task

import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(5)
    def index(self):
        self.client.get("/")
        
    @task(1)
    def predict(self):
        images = ['dog.jpeg', 
                  'gato.jpeg', 
                  'gato2.jpg', 
                  'maradona.jpg', 
                  'messi.png', 
                  'mountain.jpeg',
                  'pato.jpeg',
                  'perro.jpeg']

        n = random.randint(0,7)

        files = [
            ("file", (images[n], open("./images/"+images[n], "rb"), "image/jpeg"))
        ]
        self.client.post("/predict", files=files)