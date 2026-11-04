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
| ~50 ortak malzeme listesi + arama | Çalışıyor |
| Fotoğraf yükleme (JPEG/PNG, en çok 10 MB, kaydedilmez) | Çalışıyor |
| Yapay zekâ ile tanıma | **Sahte (mock) sağlayıcı.** Prompt ve cevap ayrıştırma hazır; gerçek sağlayıcı seçilmedi |
| Tarif eşleştirme (çok malzeme tutan önce, eksikler gösterilir) | Çalışıyor, testli |
| Favoriler | Çalışıyor, testli |
| Admin tarif ekle/düzenle/sil (API) | Çalışıyor, testli. **Admin sayfası (arayüz) yok** |
| TheMealDB içe aktarma betiği | Yazıldı, **denenmedi** (geliştirme ortamında internet kısıtlıydı) |
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

1. **Talha:** Görsel destekli bir yapay zekâ sağlayıcısı seç (ücretsiz/öğrenci kotası). `vision.py` içinde `VisionProvider` alt sınıfı yaz, `get_provider`'a ekle. Tek çağrı, tekrar yok, ~25 sn zaman aşımı.
2. **İdil:** `python -m scripts.import_themealdb` çalıştır; malzeme adlarının ortak listeyle uyuştuğunu kontrol et (ör. TheMealDB "chicken breast" der, liste "chicken" der → eşleştirme tablosu gerekebilir). TheMealDB lisans/atıf şartını rapora yaz.
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
uvicorn app.main:app --reload        # http://localhost:8000/docs
pytest -q                            # testler
```
PostgreSQL kullanmak için `.env.example` dosyasını `.env` olarak kopyalayıp `DATABASE_URL` girin.
Bir kullanıcıyı admin yapmak: `python -m scripts.make_admin email@ornek.com`

**Frontend** (Node 22):
```bash
cd frontend
npm install
npm run dev                          # http://localhost:5173 (API'ye otomatik bağlanır)
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
