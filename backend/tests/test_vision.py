import pytest

from app.services.vision import VisionError, build_prompt, parse_response


def test_prompt_lists_allowed_ingredients():
    p = build_prompt(["egg", "milk"])
    assert "egg, milk" in p and "sure" in p and "unsure" in p


def test_parse_filters_unknown_and_duplicates():
    out = parse_response('Here: {"sure": ["Egg", "dragon fruit", "egg"], "unsure": ["milk", "egg"]}', ["egg", "milk"])
    assert out == {"sure": ["egg"], "unsure": ["milk"]}


def test_parse_bad_json_raises():
    with pytest.raises(VisionError):
        parse_response("no json here")
