from locust import HttpUser, User, TaskSet, task

class BookStoreLocustTasks(TaskSet):
    # @task
    # def token_task(self):
    #     self.client.post("/token", dict(username="user1", password="test"))

    @task
    def test_post_user(self):
        user_dict = {
            "name":"personal",
            "password":"pass1",
            "role":"admin",
            "mail":"a@b.com"
        }
        auth_header = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTYxMTU3MzY0Mn0.CYQcF21vhv3Co4wkY_JtDte06GpTfSoKrg-y1qg7x3U"}
        self.client.post("/v1/user", json=user_dict, headers=auth_header)

class BookstoreLoadTest(HttpUser):
    tasks = [ BookStoreLocustTasks ]
    host = 'http://localhost:3000'
