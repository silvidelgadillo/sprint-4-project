from locust import TaskSet, task, HttpUser, between

class UserBehavior(TaskSet):
    # Put your stress tests here
    # TODO
    # raise NotImplementedError

    @task(1)
    ## call the "page" like a reload
    ## 1 excute this task only once
    def index(self):
        self.client.get('http://localhost/')

    @task(3)
    # what servidor has to do with clients
    ## executed 3 times
    ## automatization
    def predict(self):
        ## recive a file type image jpg, and dog image, open it. Send it to the local host
        file = [
            ('file', ('dog.jpeg', open('dog.jpeg','rb'), 'image/jpeg'))
        ]
        headers = {}
        payload = {}
        self.client.post('http://localhost/predict',
            headers = headers,
            data = payload,
            files = file,
        )


class APIUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1,10)
# older version
#    min_wait = 1000
#    max_wait = 5000
