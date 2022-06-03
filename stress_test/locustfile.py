from locust import HttpUser, TaskSet, task

class UserBehavior(HttpUser):

    # Put your stress tests here
    # TODO
    # task_set = UserBehavior
    # max_wait = 5000
    # min_wait = 1000

    @task(1)
    def index(self):
        self.client.get('http://localhost/')
        # self.client.get('http://0.0.0.0/')
    
    @task(2)
    def predict(self):
        file = [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
        self.client.post('http://localhost/predict', headers = {}, data = {}, files = file)

# class APIUser(HttpUser):
#     task = UserBehavior
#     max_wait = 5000
#     min_wait = 1000