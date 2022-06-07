from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
       
      
    @task
    def index(self):
        self.client.get("http://localhost/")
       
        
    @task
    def predict(self):
        files= [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
        self.client.post("http://localhost/predict", headers={}, data={}, files=files)

class APIUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(
        1, 5
    )
