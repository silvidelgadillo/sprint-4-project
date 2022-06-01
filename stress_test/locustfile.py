from locust import task, between, HttpUser


class UserBehavior(HttpUser):
    # Put your stress tests here
    # TODO
    wait_time = between(1, 5)

    @task(10)
    def index(self):
        self.client.get('http://127.0.0.1/')

    @task(30)
    def predict(self):
        files = [
            ('file', ('dog.jpeg', open('dog.jpeg','rb'), 'image/jpeg'))
        ]
        headers = {}
        payload = {}
        self.client.post(
            'http://0.0.0.0/predict',
            headers = headers,
            data = payload,
            files = files,
        )

    # @task(10)
    # def press_page(self):
    #     with open('dog.jpeg', 'rb') as image:
    #         self.client.post("/predict", files={'file':image})


# class APIUser(HttpLocust):
#     task_set = UserBehavior
#     min_wait = 1000
#     max_wait = 5000