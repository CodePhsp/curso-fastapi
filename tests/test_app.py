from fastapi.testclient import TestClient

from curso_fastapi.app import app

client = TestClient(app)
