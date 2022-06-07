from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):

    # Put your stress tests here
    @task
    def predict_post(self):
        with open("dog.jpeg", "rb") as file:
            url = 'http://localhost/predict'
            filename = 'dog.jpeg'
            headers = {
                    # 'User-Agent': 'curl/7.58.0',
                    # 'Cookie': 'authsomething=datastring; othercookie=datastring',
            }
            files = [
                ("image", (filename, file, "image/jpeg")),
            ]
            response = self.client.post(url, headers=headers, files=files)
    @task
    def index_get(self):
        url = 'http://localhost'
        response = self.client.get(url)
class MyLocust(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)