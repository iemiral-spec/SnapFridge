"""Fotoğraftan malzeme tanıma. Sahibi: Talha (WBS-3.2).

Kurallar (plan):
- Her fotoğraf için TEK yapay zekâ çağrısı, otomatik tekrar yok.
- Yapay zekâ SADECE ortak malzeme listesinden seçer.
- Sonuç iki grup: "sure" (emin) ve "unsure" (emin değil).

Hangi sağlayıcının (vision LLM) kullanılacağı ekip kararı, henüz seçilmedi.
Yeni sağlayıcı eklemek için `VisionProvider` alt sınıfı yazıp `get_provider`'a ekleyin.
`build_prompt` ve `parse_response` sağlayıcıdan bağımsızdır ve test edilmiştir.
"""
import json
import re

from ..config import settings
from ..ingredients_list import COMMON_INGREDIENTS, normalize


class VisionError(Exception):
    """Kullanıcıya gösterilebilir hata: arayüz manuel seçime düşer."""


def build_prompt(allowed: list[str] = COMMON_INGREDIENTS) -> str:
    return (
        "You see a photo of a fridge or kitchen counter. Identify food ingredients that are visible.\n"
        "Choose ONLY from this list (use the exact spelling): " + ", ".join(allowed) + ".\n"
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
    def recognize(self, image: bytes, content_type: str) -> dict[str, list[str]]:
        raise NotImplementedError


class MockVisionProvider(VisionProvider):
    """Geliştirme ve testler için: API anahtarı gerektirmez, sabit bir sonuç döner."""

    def recognize(self, image: bytes, content_type: str) -> dict[str, list[str]]:
        return parse_response('{"sure": ["egg", "milk", "tomato"], "unsure": ["cheese"]}')


def get_provider() -> VisionProvider:
    name = settings.vision_provider.lower()
    if name == "mock":
        return MockVisionProvider()
    # TODO (Talha, WBS-3.2): seçilen gerçek sağlayıcıyı buraya ekle (timeout ~25 sn).
    raise VisionError(f"Bilinmeyen yapay zekâ sağlayıcısı: {name}")
