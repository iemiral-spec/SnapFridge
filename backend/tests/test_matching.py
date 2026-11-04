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


def test_dataset_spellings_match_common_names():
    recipes = [RecipeLike(1, "Frittata", ["Eggs", "spring onions", "cherry tomatoes", "sea salt"])]
    res = match_recipes(["egg", "green onion", "tomato"], recipes)
    assert res[0].matched == ["egg", "green onion", "tomato"] and res[0].missing == []


def test_long_recipe_with_many_missing_does_not_beat_nearly_ready_one():
    recipes = [
        RecipeLike(1, "Big Stew", ["egg", "tomato", "onion", "a", "b", "c", "d", "e", "f", "g"]),
        RecipeLike(2, "Menemen", ["egg", "tomato", "onion", "bell pepper"]),
    ]
    res = match_recipes(["egg", "tomato", "onion"], recipes)
    assert [r.title for r in res] == ["Menemen", "Big Stew"]
