# Yapay Zekâ Kullanım Kaydı

Ders kuralı: yapay zekâ asistanlarının yaptığı iş, harcanan süre, insan inceleme süresi ve
yapay zekânın sebep olduğu hatalar kaydedilir. Yeni her kullanımda tabloya bir satır ekleyin.

| Tarih | WBS | Araç | Ne üretti | Yapay zekâ süresi | İnsan inceleme süresi | Yapay zekânın hataları / nasıl bulundu |
|---|---|---|---|---|---|---|
| 2026-11-04 | 1.2 (ve diğerlerinin iskeleti) | Claude Code | Backend (FastAPI) + DB şeması + eşleştirme + sahte vision + React arayüz + testler + CI/Render taslakları (PR: "Uygulama iskeleti") | ~1 saat | _ekip dolduracak_ | Geliştirme sırasında: testler önce gerçek veritabanını silebilecek şekilde yazılmıştı, ayrı `TEST_DATABASE_URL` ile düzeltildi. TheMealDB betiği ağ kısıtı yüzünden denenemedi. İnceleme sonrası bulunanlar: _ekip dolduracak_ |
