from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(5)
    def index(self):
        self.client.get("/")
        
    @task(1)
    def predict(self):
        files = [
            ("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))
        ]
        self.client.post("/predict", files=files)