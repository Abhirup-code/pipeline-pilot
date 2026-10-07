"""REST API tests: CRUD, validation, and error handling."""
import requests

def create(base, title="Write tests"):
    return requests.post(f"{base}/api/tasks", json={"title": title})

def test_health(base_url):
    r = requests.get(f"{base_url}/api/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}

def test_create_task_returns_201_and_body(base_url):
    r = create(base_url, "Buy milk")
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Buy milk" and body["done"] is False and "id" in body

def test_create_rejects_empty_title(base_url):
    for title in ["", "   "]:
        r = create(base_url, title)
        assert r.status_code == 400 and r.json()["error"] == "title is required"

def test_create_rejects_missing_body(base_url):
    r = requests.post(f"{base_url}/api/tasks", data="not json")
    assert r.status_code == 400

def test_create_rejects_long_title(base_url):
    assert create(base_url, "x" * 101).status_code == 400

def test_get_task_and_404(base_url):
    tid = create(base_url).json()["id"]
    assert requests.get(f"{base_url}/api/tasks/{tid}").status_code == 200
    assert requests.get(f"{base_url}/api/tasks/999999").status_code == 404

def test_update_marks_done(base_url):
    tid = create(base_url).json()["id"]
    r = requests.put(f"{base_url}/api/tasks/{tid}", json={"done": True})
    assert r.status_code == 200 and r.json()["done"] is True

def test_update_rejects_blank_title(base_url):
    tid = create(base_url).json()["id"]
    r = requests.put(f"{base_url}/api/tasks/{tid}", json={"title": " "})
    assert r.status_code == 400

def test_delete_then_get_is_404(base_url):
    tid = create(base_url).json()["id"]
    assert requests.delete(f"{base_url}/api/tasks/{tid}").status_code == 204
    assert requests.get(f"{base_url}/api/tasks/{tid}").status_code == 404
    assert requests.delete(f"{base_url}/api/tasks/{tid}").status_code == 404

def test_list_contains_created_task(base_url):
    tid = create(base_url, "Listed task").json()["id"]
    ids = [t["id"] for t in requests.get(f"{base_url}/api/tasks").json()]
    assert tid in ids
