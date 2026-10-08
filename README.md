# Pipeline Pilot

Test automation (Playwright, pytest, Locust) and a CI/CD pipeline (Docker, GitHub Actions, GHCR) for a small Flask task tracker.

A small, runnable test automation project. It tests a Flask task tracker (web page plus REST API) at three levels:

| Layer | Tool | What it covers |
|---|---|---|
| API tests | pytest + requests | CRUD, validation, 400/404 handling |
| UI end-to-end tests | Playwright (Python) | add, complete, delete, empty-title error, HTML escaping |
| Load test | Locust | 20 users, mixed read/write traffic |
| CI | GitHub Actions | runs API and UI tests, builds and smoke-tests the Docker image, pushes it to GHCR |
| Container | Docker, gunicorn | non-root image with a health check |


## Run it

```bash
pip install -r requirements.txt
playwright install chromium
pytest                      # 16 tests: 10 API, 6 UI
```

Load test (start the app in one terminal, run Locust in another):

```bash
python -m app.server
locust -f load/locustfile.py --headless -u 20 -r 10 -t 15s --host http://127.0.0.1:5000
```

## Sample load result (local machine, 15 s, 20 users)

1,166 requests, 0 failures, median 3 ms, 95th percentile 5 ms, about 78 requests/s.
This is a local baseline on a tiny in-memory app, not a production benchmark.


## Run in Docker

```bash
docker compose up --build
# http://localhost:8000
```
