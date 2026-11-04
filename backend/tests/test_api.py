def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_register_duplicate_and_bad_login(client, user_headers):
    assert client.post("/api/auth/register", json={"email": "user@test.com", "password": "secret123"}).status_code == 409
    assert client.post("/api/auth/login", data={"username": "user@test.com", "password": "wrong"}).status_code == 401
    assert client.get("/api/auth/me", headers=user_headers).json()["email"] == "user@test.com"


def test_common_ingredients_about_fifty(client):
    items = client.get("/api/ingredients/common").json()
    assert 40 <= len(items) <= 60 and len(set(items)) == len(items)


def test_search_ingredients(client):
    assert "tomato paste" in client.get("/api/ingredients/search", params={"q": "tomato"}).json()


def test_recognize_requires_login(client):
    r = client.post("/api/recognize", files={"photo": ("a.jpg", b"x", "image/jpeg")})
    assert r.status_code == 401


def test_recognize_rejects_wrong_type(client, user_headers):
    r = client.post("/api/recognize", headers=user_headers, files={"photo": ("a.gif", b"GIF89a", "image/gif")})
    assert r.status_code == 415


def test_recognize_rejects_big_file(client, user_headers):
    big = b"0" * (10 * 1024 * 1024 + 1)
    r = client.post("/api/recognize", headers=user_headers, files={"photo": ("a.jpg", big, "image/jpeg")})
    assert r.status_code == 413


def test_recognize_mock_returns_sure_and_unsure(client, user_headers):
    r = client.post("/api/recognize", headers=user_headers, files={"photo": ("a.png", b"\x89PNG", "image/png")})
    assert r.status_code == 200
    body = r.json()
    assert "egg" in body["sure"] and "cheese" in body["unsure"]


def test_match_and_detail(client, sample_recipes):
    res = client.post("/api/recipes/match", json={"ingredients": ["egg", "milk"]}).json()
    assert res[0]["title"] == "Omelette" and res[0]["missing"] == ["butter"]
    detail = client.get(f"/api/recipes/{res[0]['id']}").json()
    assert {i["name"] for i in detail["ingredients"]} == {"egg", "milk", "butter"}
    assert client.get("/api/recipes/9999").status_code == 404


def test_favorites_no_duplicates_and_private(client, sample_recipes, user_headers, other_headers):
    rid = sample_recipes[0]
    assert client.put(f"/api/favorites/{rid}", headers=user_headers).status_code == 204
    assert client.put(f"/api/favorites/{rid}", headers=user_headers).status_code == 204
    assert len(client.get("/api/favorites", headers=user_headers).json()) == 1
    assert client.get("/api/favorites", headers=other_headers).json() == []
    assert client.delete(f"/api/favorites/{rid}", headers=user_headers).status_code == 204
    assert client.get("/api/favorites", headers=user_headers).json() == []


def test_admin_crud_and_user_denied(client, user_headers, admin_headers):
    body = {"title": "Toast", "ingredients": [{"name": "bread"}, {"name": "butter"}]}
    assert client.post("/api/admin/recipes", json=body, headers=user_headers).status_code == 403
    created = client.post("/api/admin/recipes", json=body, headers=admin_headers)
    assert created.status_code == 201
    rid = created.json()["id"]
    body["title"] = "Butter Toast"
    assert client.put(f"/api/admin/recipes/{rid}", json=body, headers=admin_headers).json()["title"] == "Butter Toast"
    assert client.delete(f"/api/admin/recipes/{rid}", headers=user_headers).status_code == 403
    assert client.delete(f"/api/admin/recipes/{rid}", headers=admin_headers).status_code == 204
    assert client.get(f"/api/recipes/{rid}").status_code == 404
