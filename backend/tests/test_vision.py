import base64
from types import SimpleNamespace

import anthropic
import httpx2
import pytest

from app.services.vision import ClaudeVisionProvider, VisionError, build_prompt, parse_response, response_schema


def test_prompt_lists_allowed_ingredients():
    p = build_prompt(["egg", "milk"])
    assert "egg, milk" in p and "sure" in p and "unsure" in p


def test_parse_filters_unknown_and_duplicates():
    out = parse_response('Here: {"sure": ["Egg", "dragon fruit", "egg"], "unsure": ["milk", "egg"]}', ["egg", "milk"])
    assert out == {"sure": ["egg"], "unsure": ["milk"]}


def test_parse_bad_json_raises():
    with pytest.raises(VisionError):
        parse_response("no json here")


def test_schema_only_allows_list_items():
    schema = response_schema(["egg", "milk"])
    assert schema["properties"]["sure"]["items"]["enum"] == ["egg", "milk"]
    assert schema["additionalProperties"] is False


class _FakeMessages:
    def __init__(self, response=None, error=None):
        self.response, self.error, self.calls = response, error, []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.response


def _provider(fake):
    p = ClaudeVisionProvider(api_key="test-key")
    p.client = SimpleNamespace(beta=SimpleNamespace(messages=fake))
    return p


def test_claude_provider_sends_image_and_parses_answer():
    text = SimpleNamespace(type="text", text='{"sure": ["tomato", "onion"], "unsure": ["carrot"]}')
    fake = _FakeMessages(SimpleNamespace(stop_reason="end_turn", content=[text]))
    out = _provider(fake).recognize(b"\x89PNG", "image/png")
    assert out == {"sure": ["tomato", "onion"], "unsure": ["carrot"]}
    image = fake.calls[0]["messages"][0]["content"][0]
    assert image["source"]["media_type"] == "image/png"
    assert image["source"]["data"] == base64.standard_b64encode(b"\x89PNG").decode()


def test_claude_provider_refusal_raises():
    fake = _FakeMessages(SimpleNamespace(stop_reason="refusal", content=[]))
    with pytest.raises(VisionError):
        _provider(fake).recognize(b"x", "image/jpeg")


def test_claude_provider_timeout_raises_vision_error():
    request = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
    fake = _FakeMessages(error=anthropic.APITimeoutError(request))
    with pytest.raises(VisionError, match="zamanında"):
        _provider(fake).recognize(b"x", "image/jpeg")


def test_claude_provider_needs_key():
    with pytest.raises(VisionError):
        ClaudeVisionProvider(api_key="")
