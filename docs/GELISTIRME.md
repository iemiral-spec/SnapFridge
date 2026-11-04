# SnapFridge – Geliştirme Rehberi

Bu dosya kod iskeletini, nasıl çalıştırılacağını ve **hangi parçanın kime ait olduğunu** anlatır.

> **Yapay zekâ kullanımı:** Bu iskeletin ilk sürümü (4 Kasım 2026) İdil'in isteğiyle
> Claude Code (yapay zekâ kodlama asistanı) tarafından yazıldı. Ders kuralı gereği
> `docs/AI_KULLANIM.md` dosyasına kaydedildi. Ekip, kodu gözden geçirip sahiplenmeli.

## Ne hazır?

| Parça | Durum |
|---|---|
| Kayıt, giriş (JWT), User/Admin rolü | Çalışıyor, testli |
| Veritabanı şeması (users, ingredients, recipes, recipe_ingredients, favorites) | Çalışıyor (SQLite + PostgreSQL'de test edildi) |
| 78 ortak malzeme listesi + arama (Türkçe de aranabilir) | Çalışıyor. Veri setindeki farklı yazımlar `ALIASES` ile ortak adlara çevrilir |
| Fotoğraf yükleme (JPEG/PNG, en çok 10 MB, kaydedilmez) | Çalışıyor |
| Yapay zekâ ile tanıma | Google Gemini (ücretsiz anahtar) ya da Claude (ücretli) ile çalışıyor. Anahtar yoksa `mock` kullanılır, arayüz "Demo modu" uyarısı gösterir |
| Tarif eşleştirme (puan = tutan malzeme − eksik/2, eksikler gösterilir) | Çalışıyor, testli |
| Favoriler | Çalışıyor, testli |
| Admin tarif ekle/düzenle/sil (API) | Çalışıyor, testli. **Admin sayfası (arayüz) yok** |
| TheMealDB içe aktarma betiği | Çalışıyor: 790 tarif, resimleriyle |
| React arayüzü (giriş, malzeme seçimi, sonuçlar, detay, favoriler) | Çalışıyor |
| GitHub Actions CI, Render ayar dosyası | Taslak, ilk çalıştırmada kontrol edilmeli |

## Kim neyi sahiplenir? (Proje Planı WBS'ine göre)

| Kişi | Dosyalar | WBS |
|---|---|---|
| **Biray** (PM + backend) | `backend/app/security.py`, `routers/auth.py`, `routers/ingredients.py` içindeki `/recognize` yükleme kısmı, uçtan uca entegrasyon | 2.1, 3.1, 5.1 |
| **Ahmet İlker** (konfig. + frontend) | `frontend/` tamamı, `config.py`, `.github/workflows/ci.yml` | 1.2, 4.2 |
| **Umut** (test + backend) | `backend/tests/`, `routers/favorites.py`, `render.yaml` ve deploy | 1.1, 5.2, 6.2 |
| **Talha** (doküman + yapay zekâ) | `services/vision.py` (gerçek sağlayıcı), `ingredients_list.py`, `docs/AI_KULLANIM.md` | 3.2, 7.1 |
| **İdil** (iletişim + veritabanı) | `models.py`, `database.py`, `services/matching.py`, `services/recipes.py`, `scripts/`, `routers/recipes.py`, `routers/admin.py` | 2.2, 4.1, 6.1 |

## Sıradaki işler (TODO)

1. **Talha:** Gemini/Claude sağlayıcılarını (`vision.py`) gözden geçir, farklı buzdolabı fotoğraflarıyla dene. Prompt'u iyileştir.
2. **İdil:** `ALIASES` tablosunu genişlet (sık geçen ama eşlenmeyen adlar). TheMealDB lisans/atıf şartını rapora yaz.
3. **İdil:** Admin arayüz sayfası (`/admin`).
4. **Umut:** Render'a ilk deploy; CI'ın yeşil olduğunu kontrol et.
5. **Ahmet İlker:** Arayüzü güzelleştir, mobil görünümü kontrol et.
6. Şema değişmeye başlayınca Alembic migration'a geçin (şu an tablolar uygulama açılınca otomatik kuruluyor).

## Çalıştırma (yerel)

**Backend** (Python 3.12+):
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m scripts.seed_sample        # 8 örnek tarif (SQLite: snapfridge.db)
python -m scripts.import_themealdb   # 790 gerçek tarif (internet gerekir, ~5 sn)
uvicorn app.main:app --reload        # http://localhost:8000/docs
pytest -q                            # testler
```
Gerçek fotoğraf tanıma için `.env.example` dosyasını `.env` olarak kopyalayıp `VISION_PROVIDER=gemini` ve
`GEMINI_API_KEY=...` girin. Ücretsiz anahtar: aistudio.google.com/apikey (Google hesabı yeterli, kart istemez).
`.env` asla commit edilmez.
PostgreSQL kullanmak için aynı dosyada `DATABASE_URL` girin.
**Not:** Şema değişti (`recipe_ingredients.label`). Eski `snapfridge.db` varsa silip yukarıdaki iki betiği tekrar çalıştırın.
Bir kullanıcıyı admin yapmak: `python -m scripts.make_admin email@ornek.com`

**Frontend** (Node 22):
```bash
cd frontend
npm install
npm run dev                          # http://localhost:5173 (API'ye otomatik bağlanır)
npm run dev -- --host                # telefondan denemek için: aynı Wi-Fi'de "Network" adresini açın
```

## API özeti

| Metot | Yol | Giriş gerekli? | Açıklama |
|---|---|---|---|
| POST | `/api/auth/register` | Hayır | Kayıt |
| POST | `/api/auth/login` | Hayır | Giriş (form: username=e-posta, password) → token |
| GET | `/api/auth/me` | Evet | Kendi bilgilerim |
| GET | `/api/ingredients/common` | Hayır | ~50 ortak malzeme |
| GET | `/api/ingredients/search?q=` | Hayır | Malzeme arama |
| POST | `/api/recognize` | Evet | Fotoğraf → `{sure: [...], unsure: [...]}` |
| POST | `/api/recipes/match` | Hayır | `{ingredients: [...]}` → sıralı tarifler, eksikler |
| GET | `/api/recipes/{id}` | Hayır | Tarif detayı |
| GET/PUT/DELETE | `/api/favorites[/{id}]` | Evet | Favoriler |
| POST/PUT/DELETE | `/api/admin/recipes[/{id}]` | Admin | Tarif yönetimi |

Ayrıntılı ve denenebilir liste: backend çalışırken `http://localhost:8000/docs`.
