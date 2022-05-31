from locust import HttpLocust, HttpUser, task


class UserBehavior(HttpUser):
    #wait_time = between(1,5)
    # Put your stress tests here
    # TODO
    @task(1)
    def index(self):
        self.client.get("/")

    #raise NotImplementedError


#class APIUser(HttpLocust):
#    task_set = UserBehavior
