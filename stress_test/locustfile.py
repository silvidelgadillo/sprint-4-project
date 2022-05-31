from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):

    @task(1)
    def index(self):
        self.client.get('http://localhost:8000/')
   

    @task(2)
    def index(self):
        files = [
            ('file',('dog.jpeg', open('dog.jpeg','rb'), 'image/jpeg'))
        ]
        headers = {}
        payload = {}

        self.client.post('http://localhost:8000/predict',headers=headers,data=payload,files=files)
    

class APIUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 5000
    max_wait = 9000