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
            'http://127.0.0.1/predict',
            headers = headers,
            data = payload,
            files = files,
        )