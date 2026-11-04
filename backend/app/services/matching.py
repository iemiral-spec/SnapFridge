"""Tarif eşleştirme. Sahibi: İdil (WBS-4.1).

Kural: puan = elde olan malzeme sayısı - eksik malzeme sayısının yarısı.
Böylece çok malzeme tutan tarif öne çıkar ama 15 eksiği olan dev bir tarif,
neredeyse hazır olan kısa bir tarifi geçemez. Eşitlikte eksiği az olan önce gelir. Temel kiler malzemeleri (tuz, su...)
eksik sayılmaz. Saf fonksiyon: veritabanına dokunmaz, kolay test edilir.
"""
from dataclasses import dataclass

from ..ingredients_list import PANTRY_STAPLES, canonical


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
    have = {canonical(i) for i in user_ingredients if i.strip()}
    results: list[MatchResult] = []
    for r in recipes:
        needed = [n for n in dict.fromkeys(canonical(x) for x in r.ingredient_names) if n not in PANTRY_STAPLES]
        if not needed:
            continue
        matched = [n for n in needed if n in have]
        if not matched:
            continue  # hiçbir malzeme tutmuyorsa gösterme
        missing = [n for n in needed if n not in have]
        results.append(MatchResult(r.id, r.title, r.image_url, matched, missing, round(len(matched) / len(needed), 3)))
    results.sort(key=lambda m: (-(len(m.matched) - len(m.missing) / 2), len(m.missing), m.title))
    return results[:limit]
