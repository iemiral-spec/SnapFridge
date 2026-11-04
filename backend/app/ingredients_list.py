"""Ortak malzeme listesi. Yapay zekâ SADECE bu listeden seçebilir.

Sahibi: Talha (WBS-3.2) + İdil. Veri setindeki (TheMealDB) farklı yazımlar
`ALIASES` ile bu listedeki adlara çevrilir ("eggs" -> "egg", "spring onions" -> "green onion").
"""

COMMON_INGREDIENTS: list[str] = [
    # Süt ürünleri ve yumurta
    "egg", "milk", "butter", "cheese", "feta", "parmesan", "mozzarella", "cream cheese",
    "yogurt", "cream", "sour cream",
    # Et, tavuk, balık
    "chicken", "beef", "minced meat", "lamb", "pork", "sausage", "bacon", "ham",
    "fish", "salmon", "tuna", "shrimp",
    # Sebzeler
    "tomato", "onion", "green onion", "garlic", "potato", "sweet potato", "carrot",
    "bell pepper", "chili pepper", "cucumber", "lettuce", "spinach", "kale", "broccoli",
    "cauliflower", "cabbage", "zucchini", "eggplant", "mushroom", "corn", "peas",
    "green beans", "celery", "leek", "beetroot", "radish", "pumpkin", "olives",
    # Meyveler
    "lemon", "lime", "apple", "banana", "orange", "avocado", "strawberry",
    # Kiler
    "rice", "pasta", "noodles", "bread", "flour", "lentils", "chickpeas", "beans",
    "tomato paste", "olive oil", "sugar", "honey", "coconut milk", "soy sauce",
    # Otlar
    "parsley", "dill", "mint", "coriander", "basil", "ginger",
]

# Herkesin evinde varsayılan; eşleştirmede "eksik" sayılmaz.
PANTRY_STAPLES: set[str] = {"salt", "water", "black pepper", "oil", "vegetable oil"}

# Veri setindeki yazım -> listedeki ad. Listede olmayan malzemeler kendi adıyla kalır.
ALIASES: dict[str, str] = {
    # Kiler temelleri
    "pepper": "black pepper", "ground black pepper": "black pepper", "kosher salt": "salt",
    "sea salt": "salt", "warm water": "water", "boiling water": "water", "cold water": "water",
    "sunflower oil": "vegetable oil", "rapeseed oil": "vegetable oil", "canola oil": "vegetable oil",
    "ground nut oil": "vegetable oil", "groundnut oil": "vegetable oil", "corn oil": "vegetable oil",
    "extra virgin olive oil": "olive oil",
    "plain flour": "flour", "all purpose flour": "flour", "self-raising flour": "flour",
    "self raising flour": "flour", "bread flour": "flour", "strong white bread flour": "flour",
    "caster sugar": "sugar", "brown sugar": "sugar", "granulated sugar": "sugar",
    "golden caster sugar": "sugar", "light brown soft sugar": "sugar", "dark brown soft sugar": "sugar",
    "muscovado sugar": "sugar", "demerara sugar": "sugar", "white sugar": "sugar",
    "clear honey": "honey",
    "tomato puree": "tomato paste", "tinned tomatos": "tomato", "chopped tomatoes": "tomato",
    "plum tomatoes": "tomato", "cherry tomatoes": "tomato", "canned tomatoes": "tomato",
    "basmati rice": "rice", "jasmine rice": "rice", "long grain rice": "rice", "arborio risotto rice": "rice",
    "brown rice": "rice", "rice noodles": "noodles", "egg noodles": "noodles",
    "spaghetti": "pasta", "penne rigate": "pasta", "macaroni": "pasta", "linguine pasta": "pasta",
    "fettuccine": "pasta", "farfalle": "pasta", "rigatoni": "pasta", "tagliatelle": "pasta", "lasagne sheets": "pasta",
    "baguette": "bread", "pita bread": "bread", "white bread": "bread", "bread rolls": "bread", "ciabatta": "bread",
    "kidney beans": "beans", "black beans": "beans", "cannellini beans": "beans", "haricot beans": "beans",
    "butter beans": "beans", "red lentils": "lentils", "green red lentils": "lentils",
    "dark soy sauce": "soy sauce", "light soy sauce": "soy sauce",
    # Süt ürünleri ve yumurta
    "eggs": "egg", "egg yolks": "egg", "egg yolk": "egg", "egg white": "egg", "egg whites": "egg",
    "free-range egg, beaten": "egg", "free-range eggs, beaten": "egg",
    "unsalted butter": "butter", "melted butter": "butter", "salted butter": "butter",
    "whole milk": "milk", "semi-skimmed milk": "milk",
    "double cream": "cream", "heavy cream": "cream", "single cream": "cream", "whipping cream": "cream",
    "creme fraiche": "sour cream",
    "greek yogurt": "yogurt", "natural yogurt": "yogurt", "plain yogurt": "yogurt",
    "cheddar cheese": "cheese", "gruyère": "cheese", "gruyere": "cheese", "parmesan cheese": "parmesan",
    "parmigiano-reggiano": "parmesan", "feta cheese": "feta",
    # Et, tavuk, balık
    "chicken breast": "chicken", "chicken breasts": "chicken", "chicken thighs": "chicken",
    "chicken legs": "chicken", "chicken wings": "chicken", "chicken drumsticks": "chicken", "whole chicken": "chicken",
    "ground beef": "minced meat", "minced beef": "minced meat", "lamb mince": "minced meat",
    "minced pork": "minced meat", "ground pork": "minced meat", "beef brisket": "beef",
    "sirloin steak": "beef", "beef fillet": "beef", "stewing beef": "beef", "lamb leg": "lamb",
    "lamb shoulder": "lamb", "pork chops": "pork", "pork belly": "pork", "pork shoulder": "pork",
    "sausages": "sausage", "chorizo": "sausage", "streaky bacon": "bacon", "smoked salmon": "salmon",
    "salmon fillets": "salmon", "white fish": "fish", "white fish fillets": "fish", "cod": "fish",
    "haddock": "fish", "prawns": "shrimp", "king prawns": "shrimp", "raw king prawns": "shrimp", "tiger prawns": "shrimp",
    # Sebzeler
    "red onions": "onion", "red onion": "onion", "onions": "onion", "white onion": "onion",
    "shallots": "onion", "shallot": "onion", "challots": "onion",
    "spring onions": "green onion", "spring onion": "green onion", "scallions": "green onion",
    "garlic clove": "garlic", "garlic cloves": "garlic", "minced garlic": "garlic",
    "red pepper": "bell pepper", "green pepper": "bell pepper", "yellow pepper": "bell pepper",
    "red peppers": "bell pepper", "orange pepper": "bell pepper",
    "red chilli": "chili pepper", "green chilli": "chili pepper", "chilli": "chili pepper",
    "jalapeno": "chili pepper", "scotch bonnet": "chili pepper", "bird's-eye chillies": "chili pepper",
    "courgettes": "zucchini", "courgette": "zucchini", "aubergine": "eggplant", "egg plants": "eggplant",
    "sweetcorn": "corn", "frozen peas": "peas", "baby spinach": "spinach", "white cabbage": "cabbage",
    "red cabbage": "cabbage", "savoy cabbage": "cabbage", "iceberg lettuce": "lettuce",
    "little gem lettuce": "lettuce", "rocket": "lettuce", "beetroot": "beetroot", "beet": "beetroot",
    "black olives": "olives", "green olives": "olives", "kalamata olives": "olives",
    "celery stalk": "celery", "leeks": "leek", "sweet potatoes": "sweet potato",
    "new potatoes": "potato", "floury potatoes": "potato", "baby new potatoes": "potato",
    # Meyveler
    "lemon juice": "lemon", "lemon zest": "lemon", "lime juice": "lime", "apples": "apple",
    "bramley apples": "apple", "strawberries": "strawberry", "orange zest": "orange",
    # Otlar
    "coriander leaves": "coriander", "cilantro": "coriander", "fresh coriander": "coriander",
    "basil leaves": "basil", "fresh basil": "basil", "mint leaves": "mint", "fresh mint": "mint",
    "flat leaf parsley": "parsley", "fresh parsley": "parsley", "ground ginger": "ginger",
}

_KNOWN = set(COMMON_INGREDIENTS) | PANTRY_STAPLES


def normalize(name: str) -> str:
    return " ".join(name.strip().lower().split())


def canonical(name: str) -> str:
    """Malzeme adını listedeki tek bir yazıma çevirir (eşleştirme bunun üzerinden yapılır)."""
    n = normalize(name)
    if n in ALIASES:
        return ALIASES[n]
    for suffix in ("es", "s"):  # basit çoğul: tomatoes -> tomato, carrots -> carrot
        if n.endswith(suffix) and n[: -len(suffix)] in _KNOWN:
            return n[: -len(suffix)]
    return n
