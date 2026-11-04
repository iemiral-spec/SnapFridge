"""Ortak malzeme listesi (~50). Yapay zekâ SADECE bu listeden seçebilir.

Sahibi: Talha (WBS-3.2) + İdil. İsimler veri setindeki (TheMealDB) adlarla uyumlu
olmalı; veri seti içe aktarılınca bu liste gözden geçirilecek.
"""

COMMON_INGREDIENTS: list[str] = [
    # Süt ürünleri ve yumurta
    "egg", "milk", "butter", "cheese", "yogurt", "cream",
    # Et, tavuk, balık
    "chicken", "beef", "minced meat", "sausage", "bacon", "fish", "tuna", "shrimp",
    # Sebzeler
    "tomato", "onion", "garlic", "potato", "carrot", "bell pepper", "chili pepper",
    "cucumber", "lettuce", "spinach", "broccoli", "cabbage", "zucchini", "eggplant",
    "mushroom", "corn", "peas", "green beans",
    # Meyveler
    "lemon", "apple", "banana", "orange", "avocado",
    # Kiler
    "rice", "pasta", "bread", "flour", "lentils", "chickpeas", "beans",
    "tomato paste", "olive oil", "sugar", "honey",
    # Otlar
    "parsley", "basil", "ginger",
]

# Herkesin evinde varsayılan; eşleştirmede "eksik" sayılmaz.
PANTRY_STAPLES: set[str] = {"salt", "water", "black pepper", "oil", "vegetable oil"}


def normalize(name: str) -> str:
    return " ".join(name.strip().lower().split())
