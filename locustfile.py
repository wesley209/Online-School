from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:8000"  # Remplacez par l'URL de votre application
    wait_time = between(1, 5)

    @task
    def load_homepage(self):
        self.client.get("/")
