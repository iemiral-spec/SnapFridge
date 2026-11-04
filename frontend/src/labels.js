// Malzemelerin Türkçe adları. Backend İngilizce ad kullanır (eşleştirme için);
// arayüz burada karşılığı olanları Türkçe gösterir, olmayanları olduğu gibi bırakır.
const TR = {
  egg: "yumurta", milk: "süt", butter: "tereyağı", cheese: "peynir", feta: "beyaz peynir",
  parmesan: "parmesan", mozzarella: "mozzarella", "cream cheese": "krem peynir", yogurt: "yoğurt",
  cream: "krema", "sour cream": "ekşi krema",
  chicken: "tavuk", beef: "dana eti", "minced meat": "kıyma", lamb: "kuzu eti", pork: "domuz eti",
  sausage: "sosis / sucuk", bacon: "pastırma / bacon", ham: "jambon", fish: "balık", salmon: "somon",
  tuna: "ton balığı", shrimp: "karides",
  tomato: "domates", onion: "soğan", "green onion": "yeşil soğan", garlic: "sarımsak", potato: "patates",
  "sweet potato": "tatlı patates", carrot: "havuç", "bell pepper": "dolmalık biber", "chili pepper": "acı biber",
  cucumber: "salatalık", lettuce: "marul / yeşillik", spinach: "ıspanak", kale: "kara lahana",
  broccoli: "brokoli", cauliflower: "karnabahar", cabbage: "lahana", zucchini: "kabak", eggplant: "patlıcan",
  mushroom: "mantar", corn: "mısır", peas: "bezelye", "green beans": "taze fasulye", celery: "kereviz sapı",
  leek: "pırasa", beetroot: "pancar", radish: "turp", pumpkin: "bal kabağı", olives: "zeytin",
  lemon: "limon", lime: "misket limonu", apple: "elma", banana: "muz", orange: "portakal",
  avocado: "avokado", strawberry: "çilek",
  rice: "pirinç", pasta: "makarna", noodles: "erişte / noodle", bread: "ekmek", flour: "un",
  lentils: "mercimek", chickpeas: "nohut", beans: "kuru fasulye", "tomato paste": "salça",
  "olive oil": "zeytinyağı", sugar: "şeker", honey: "bal", "coconut milk": "hindistan cevizi sütü",
  "soy sauce": "soya sosu",
  salt: "tuz", "black pepper": "karabiber", water: "su", oil: "yağ", "vegetable oil": "sıvı yağ",
  parsley: "maydanoz", dill: "dereotu", mint: "nane", coriander: "kişniş", basil: "fesleğen", ginger: "zencefil",
};

export const tr = (name) => TR[name] || name;

// Arama kutusu için: Türkçe yazılınca İngilizce adı bulur ("domat" -> "tomato").
const fold = (s) => s.toLocaleLowerCase("tr").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ı/g, "i");
export const searchTr = (q) => {
  const f = fold(q);
  return Object.keys(TR).filter((k) => fold(TR[k]).includes(f));
};
