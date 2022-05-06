from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    # Put your stress tests here
    # TODO
    raise NotImplementedError


class APIUser(HttpLocust):
    task_set = UserBehavior
