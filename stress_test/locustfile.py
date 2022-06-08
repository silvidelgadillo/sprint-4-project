from locust import HttpUser, task, between


class UserBehavior(HttpUser):
  wait_time = between(1,5)

    # Put your stress tests here
    # TODO
  @task(1)
  def index(self):
    self.client.get('http://localhost/')
  
  @task(2)
  def predict(self):
    with open("dog.jpeg", "rb") as img:
      file = {"file": img}
      self.client.post("http://localhost/predict", headers = {}, data = {}, files = file)
