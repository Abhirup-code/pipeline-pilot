import threading, time
import pytest, requests
from werkzeug.serving import make_server
from app.server import create_app

PORT = 5055
BASE = f"http://127.0.0.1:{PORT}"

@pytest.fixture(scope="session")
def base_url():
    srv = make_server("127.0.0.1", PORT, create_app())
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    for _ in range(50):
        try:
            requests.get(BASE + "/api/health", timeout=0.5); break
        except requests.ConnectionError:
            time.sleep(0.1)
    yield BASE
    srv.shutdown()
