"""Fotoğraftan malzeme tanıma. Sahibi: Talha (WBS-3.2).

Kurallar (plan):
- Her fotoğraf için TEK yapay zekâ çağrısı, otomatik tekrar yok.
- Yapay zekâ SADECE ortak malzeme listesinden seçer.
- Sonuç iki grup: "sure" (emin) ve "unsure" (emin değil).

Sağlayıcılar (.env içindeki VISION_PROVIDER):
- "claude": Anthropic Claude (gerçek tanıma, ANTHROPIC_API_KEY gerekir)
- "mock":   API anahtarı olmadan geliştirme/test; her fotoğrafa AYNI cevabı verir.
`build_prompt` ve `parse_response` sağlayıcıdan bağımsızdır ve test edilmiştir.
"""
import base64
import json
import re

import anthropic

from ..config import settings
from ..ingredients_list import COMMON_INGREDIENTS, normalize


class VisionError(Exception):
    """Kullanıcıya gösterilebilir hata: arayüz manuel seçime düşer."""


def build_prompt(allowed: list[str] = COMMON_INGREDIENTS) -> str:
    return (
        "You see a photo of a fridge, a fridge drawer or a kitchen counter. Identify the food ingredients "
        "that are visible, including items in packages, jars or bottles when the label or shape makes them clear.\n"
        "Choose ONLY from this list (use the exact spelling): " + ", ".join(allowed) + ".\n"
        "Map close variants to the nearest list item (e.g. cherry tomatoes -> tomato, red onion -> onion, "
        "scallions -> green onion, any lettuce or salad leaves -> lettuce).\n"
        "Put an item in \"sure\" if it is clearly visible, in \"unsure\" if you think it is there but "
        "are not certain. Do not list anything that is not in the list.\n"
        'Answer with JSON only, like: {"sure": ["egg"], "unsure": ["cheese"]}'
    )


def parse_response(text: str, allowed: list[str] = COMMON_INGREDIENTS) -> dict[str, list[str]]:
    """Model cevabını güvenle ayrıştırır; listede olmayanları atar, tekrarları temizler."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise VisionError("Yapay zekâ cevabı okunamadı.")
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise VisionError("Yapay zekâ cevabı okunamadı.") from exc
    allowed_set = {normalize(a) for a in allowed}

    def clean(items) -> list[str]:
        if not isinstance(items, list):
            return []
        out = []
        for it in items:
            if isinstance(it, str) and normalize(it) in allowed_set and normalize(it) not in out:
                out.append(normalize(it))
        return out

    sure = clean(data.get("sure"))
    unsure = [i for i in clean(data.get("unsure")) if i not in sure]
    return {"sure": sure, "unsure": unsure}


class VisionProvider:
    is_demo = False

    def recognize(self, image: bytes, content_type: str) -> dict[str, list[str]]:
        raise NotImplementedError


class MockVisionProvider(VisionProvider):
    """Geliştirme ve testler için: API anahtarı gerektirmez, sabit bir sonuç döner."""

    is_demo = True

    def recognize(self, image: bytes, content_type: str) -> dict[str, list[str]]:
        return parse_response('{"sure": ["egg", "milk", "tomato"], "unsure": ["cheese"]}')


def response_schema(allowed: list[str] = COMMON_INGREDIENTS) -> dict:
    """Cevabı JSON'a ve SADECE listedeki adlara zorlar (enum)."""
    names = {"type": "array", "items": {"type": "string", "enum": allowed}}
    return {
        "type": "object",
        "properties": {"sure": names, "unsure": names},
        "required": ["sure", "unsure"],
        "additionalProperties": False,
    }


class ClaudeVisionProvider(VisionProvider):
    """Anthropic Claude ile tanıma. Plan kuralları: tek çağrı, otomatik tekrar yok, ~25 sn."""

    is_demo = False
    model = "claude-opus-5-5"

    def __init__(self, api_key: str, timeout: float = 25.0):
        if not api_key:
            raise VisionError("Yapay zekâ anahtarı (ANTHROPIC_API_KEY) ayarlanmamış.")
        self.client = anthropic.Anthropic(api_key=api_key, timeout=timeout, max_retries=0)

    def recognize(self, image: bytes, content_type: str) -> dict[str, list[str]]:
        try:
            response = self.client.beta.messages.create(
                model=self.model,
                max_tokens=4000,
                # Basit bir sınıflandırma: düşük efor hızlı cevap verir.
                output_config={"effort": "low", "format": {"type": "json_schema", "schema": response_schema()}},
                # Model bir isteği reddederse API aynı isteği uygun bir yedek modelle tekrar dener.
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {
                            "type": "base64",
                            "media_type": content_type,
                            "data": base64.standard_b64encode(image).decode(),
                        }},
                        {"type": "text", "text": build_prompt()},
                    ],
                }],
            )
        except anthropic.APITimeoutError as exc:
            raise VisionError("Yapay zekâ zamanında cevap vermedi.") from exc
        except anthropic.AuthenticationError as exc:
            raise VisionError("Yapay zekâ anahtarı geçersiz.") from exc
        except anthropic.RateLimitError as exc:
            raise VisionError("Yapay zekâ şu an çok yoğun, biraz sonra tekrar deneyin.") from exc
        except anthropic.BadRequestError as exc:
            raise VisionError("Fotoğraf yapay zekâya gönderilemedi.") from exc
        except anthropic.APIStatusError as exc:
            raise VisionError("Yapay zekâ servisinde bir hata oluştu.") from exc
        except anthropic.APIConnectionError as exc:
            raise VisionError("Yapay zekâ servisine bağlanılamadı.") from exc

        if response.stop_reason == "refusal":
            raise VisionError("Yapay zekâ bu fotoğrafı inceleyemedi.")
        text = next((b.text for b in response.content if b.type == "text"), "")
        return parse_response(text)


def get_provider() -> VisionProvider:
    name = settings.vision_provider.lower()
    if name == "mock":
        return MockVisionProvider()
    if name == "claude":
        return ClaudeVisionProvider(settings.anthropic_api_key)
    raise VisionError(f"Bilinmeyen yapay zekâ sağlayıcısı: {name}")
