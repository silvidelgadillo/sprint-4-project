from locust import HttpUser, between, task



class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
      
    @task
    def index(self):
        self.client.get("http://localhost/")
       
        
    @task
    def predict(self):
        files= [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
        self.client.post("http://localhost/predict", headers={}, data={}, files=files)

