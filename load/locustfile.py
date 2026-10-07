"""Load test: mixed read/write traffic against the task API."""
from locust import HttpUser, task, between

class TaskUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(5)
    def list_tasks(self):
        self.client.get("/api/tasks")

    @task(2)
    def create_and_read(self):
        r = self.client.post("/api/tasks", json={"title": "load task"})
        if r.status_code == 201:
            self.client.get(f"/api/tasks/{r.json()['id']}", name="/api/tasks/[id]")

    @task(1)
    def health(self):
        self.client.get("/api/health")
