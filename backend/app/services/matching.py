"""Tarif eşleştirme. Sahibi: İdil (WBS-4.1).

Basit kural: kullanıcının sahip olduğu malzeme sayısı en çok olan tarif öne çıkar.
Eşitlikte eksik malzemesi az olan önce gelir. Temel kiler malzemeleri (tuz, su...)
eksik sayılmaz. Saf fonksiyon: veritabanına dokunmaz, kolay test edilir.
"""
from dataclasses import dataclass

from ..ingredients_list import PANTRY_STAPLES, normalize


@dataclass
class RecipeLike:
    id: int
    title: str
    ingredient_names: list[str]
    image_url: str | None = None


@dataclass
class MatchResult:
    id: int
    title: str
    image_url: str | None
    matched: list[str]
    missing: list[str]
    score: float  # 0..1, sahip olunan / gerekli malzeme oranı


def match_recipes(user_ingredients: list[str], recipes: list[RecipeLike], limit: int = 20) -> list[MatchResult]:
    have = {normalize(i) for i in user_ingredients if i.strip()}
    results: list[MatchResult] = []
    for r in recipes:
        needed = [n for n in dict.fromkeys(normalize(x) for x in r.ingredient_names) if n not in PANTRY_STAPLES]
        if not needed:
            continue
        matched = [n for n in needed if n in have]
        if not matched:
            continue  # hiçbir malzeme tutmuyorsa gösterme
        missing = [n for n in needed if n not in have]
        results.append(MatchResult(r.id, r.title, r.image_url, matched, missing, round(len(matched) / len(needed), 3)))
    results.sort(key=lambda m: (-len(m.matched), len(m.missing), m.title))
    return results[:limit]
