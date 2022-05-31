from locust import HttpLocust, HttpUser, task


class UserBehavior(HttpUser):
    #wait_time = between(1,5)
    # Put your stress tests here
    # TODO
    @task(1)
    def index(self):
        self.client.get("/")
    
    @task(3)
    def predict(self):
        files = [("file",("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
        headers ={}
        payload = {}
        self.client.post(
            "http://localhost/predict",
            headers = headers,
            data = payload,
            files = files,
        )

    #raise NotImplementedError


#class APIUser(HttpLocust):
#    task_set = UserBehavior
