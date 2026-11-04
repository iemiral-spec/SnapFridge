# Yapay Zekâ Kullanım Kaydı

Ders kuralı: yapay zekâ asistanlarının yaptığı iş, harcanan süre, insan inceleme süresi ve
yapay zekânın sebep olduğu hatalar kaydedilir. Yeni her kullanımda tabloya bir satır ekleyin.

| Tarih | WBS | Araç | Ne üretti | Yapay zekâ süresi | İnsan inceleme süresi | Yapay zekânın hataları / nasıl bulundu |
|---|---|---|---|---|---|---|
| 2026-11-04 | 1.2 (ve diğerlerinin iskeleti) | Claude Code | Backend (FastAPI) + DB şeması + eşleştirme + sahte vision + React arayüz + testler + CI/Render taslakları (PR: "Uygulama iskeleti") | ~1 saat | _ekip dolduracak_ | Geliştirme sırasında: testler önce gerçek veritabanını silebilecek şekilde yazılmıştı, ayrı `TEST_DATABASE_URL` ile düzeltildi. TheMealDB betiği ağ kısıtı yüzünden denenemedi. İnceleme sonrası bulunanlar: _ekip dolduracak_ |
| 2026-11-05 | 2.2, 3.2, 4.1, 4.2 | Claude Code | Gerçek fotoğraf tanıma (Claude), malzeme listesinin 78'e çıkması + TheMealDB yazım eşleştirmesi (`ALIASES`), 790 tarifin içe aktarılması, sıralama kuralında değişiklik, Türkçe malzeme adları ve mobil arayüz iyileştirmeleri (PR: "Gerçek tanıma ve arayüz") | ~1 saat | _ekip dolduracak_ | Python 3.14'te eski paket sürümleri çalışmıyordu, sürümler yükseltildi. Sahte tanıma her fotoğrafa aynı cevabı veriyordu, kullanıcı fark etti; arayüze "Demo modu" uyarısı eklendi. Malzeme listesi plandaki ~50 sınırını aşıyor (78), test buna göre değiştirildi: ekip onaylamalı. Claude anahtarı ücretli olduğu için ücretsiz Google Gemini sağlayıcısı da eklendi (varsayılan önerilen). |
