"""Testler geçici bir SQLite veritabanı kullanır; PostgreSQL gerekmez. Sahibi: Umut (test yöneticisi)."""
import os
import tempfile

_db_file = os.path.join(tempfile.mkdtemp(), "test.db")
# Gerçek veritabanını silmemek için sadece TEST_DATABASE_URL kullanılır (CI: PostgreSQL).
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", f"sqlite:///{_db_file}")
os.environ["VISION_PROVIDER"] = "mock"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Recipe, User  # noqa: E402
from app.schemas import RecipeIn  # noqa: E402
from app.services.recipes import apply_recipe_data  # noqa: E402


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    with TestClient(app) as c:  # lifespan: tabloları kurar
        yield c


def _register_and_login(client, email: str, password: str = "secret123") -> dict:
    assert client.post("/api/auth/register", json={"email": email, "password": password}).status_code == 201
    token = client.post("/api/auth/login", data={"username": email, "password": password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def user_headers(client):
    return _register_and_login(client, "user@test.com")


@pytest.fixture()
def admin_headers(client):
    headers = _register_and_login(client, "admin@test.com")
    with SessionLocal() as db:
        db.query(User).filter(User.email == "admin@test.com").update({"is_admin": True})
        db.commit()
    return headers


@pytest.fixture()
def other_headers(client):
    return _register_and_login(client, "other@test.com")


@pytest.fixture()
def sample_recipes(client):
    data = [
        RecipeIn(title="Menemen", ingredients=[{"name": n} for n in ["egg", "tomato", "bell pepper", "onion", "salt"]]),
        RecipeIn(title="Omelette", ingredients=[{"name": n} for n in ["egg", "milk", "butter"]]),
        RecipeIn(title="Lentil Soup", ingredients=[{"name": n} for n in ["lentils", "onion", "carrot"]]),
    ]
    ids = []
    with SessionLocal() as db:
        for d in data:
            r = Recipe(source="sample")
            db.add(r)
            apply_recipe_data(db, r, d)
            db.flush()
            ids.append(r.id)
        db.commit()
    return ids
