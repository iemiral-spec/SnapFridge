from app.services.matching import RecipeLike, match_recipes

RECIPES = [
    RecipeLike(1, "Menemen", ["egg", "tomato", "bell pepper", "onion", "salt"]),
    RecipeLike(2, "Omelette", ["egg", "milk", "butter"]),
    RecipeLike(3, "Lentil Soup", ["lentils", "onion", "carrot"]),
]


def test_ranks_by_matched_count_then_missing():
    res = match_recipes(["egg", "milk", "tomato"], RECIPES)
    assert [r.title for r in res] == ["Omelette", "Menemen"]
    assert res[0].missing == ["butter"]


def test_pantry_staples_not_missing():
    res = match_recipes(["egg", "tomato", "bell pepper", "onion"], RECIPES)
    menemen = next(r for r in res if r.title == "Menemen")
    assert menemen.missing == [] and menemen.score == 1.0


def test_no_match_returns_empty():
    assert match_recipes(["banana"], RECIPES) == []


def test_case_and_space_insensitive():
    res = match_recipes(["  EGG ", "Milk"], RECIPES)
    assert res[0].title == "Omelette"
