// Ana akış: fotoğraf yükle (isteğe bağlı) → malzemeleri düzelt → tarif bul.
// Sahibi: Ahmet İlker (WBS-4.2), entegrasyon: Biray (WBS-5.1).
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api.js";
import { loadSelection, saveSelection } from "../selection.js";
import IngredientPicker from "../components/IngredientPicker.jsx";
import Tag from "../components/Tag.jsx";

export default function AnalyzePage() {
  const [common, setCommon] = useState([]);
  const [unsure, setUnsure] = useState([]);
  const [selected, setSelected] = useState(() => new Set(loadSelection()));
  const [preview, setPreview] = useState(null);
  const [found, setFound] = useState(null); // son fotoğrafta bulunan malzeme sayısı
  const [demo, setDemo] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => { api.commonIngredients().then(setCommon).catch((e) => setError(e.message)); }, []);
  useEffect(() => { saveSelection([...selected]); }, [selected]);
  useEffect(() => () => preview && URL.revokeObjectURL(preview), [preview]);

  const toggle = (name) => setSelected((prev) => {
    const next = new Set(prev);
    next.has(name) ? next.delete(name) : next.add(name);
    return next;
  });

  const onPhoto = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setError(""); setFound(null); setDemo(false); setBusy(true);
    setPreview(URL.createObjectURL(file));
    try {
      const res = await api.recognize(file);
      setSelected((prev) => new Set([...prev, ...res.sure]));
      setUnsure(res.unsure);
      setFound(res.sure.length);
      setDemo(res.demo);
    } catch (err) {
      setError(err.message);
    } finally { setBusy(false); e.target.value = ""; }
  };

  const findRecipes = () => navigate("/results", { state: { ingredients: [...selected] } });

  return (
    <div className="space-y-5 pb-24">
      <section className="bg-white p-5 rounded-2xl shadow-sm">
        <h1 className="text-xl font-bold mb-1">Buzdolabında ne var?</h1>
        <p className="text-sm text-slate-500 mb-4">Buzdolabının fotoğrafını çekin, malzemeleri biz bulalım. İsterseniz bu adımı atlayıp kendiniz seçin.</p>

        <div className="flex items-center gap-4">
          {preview && (
            <div className="relative shrink-0">
              <img src={preview} alt="Yüklenen fotoğraf" className="w-24 h-24 object-cover rounded-xl" />
              {busy && <div className="absolute inset-0 bg-white/70 rounded-xl flex items-center justify-center"><div className="w-7 h-7 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin" /></div>}
            </div>
          )}
          <label className={`flex-1 text-center bg-emerald-600 text-white px-4 py-3 rounded-xl font-medium ${busy ? "opacity-60" : "cursor-pointer active:bg-emerald-700"}`}>
            {busy ? "Fotoğraf inceleniyor…" : preview ? "📷 Başka fotoğraf" : "📷 Fotoğraf çek / yükle"}
            <input type="file" accept="image/jpeg,image/png" className="hidden" onChange={onPhoto} disabled={busy} />
          </label>
        </div>

        {found !== null && !demo && (
          <p className="text-sm text-emerald-700 mt-3">
            {found > 0 ? `${found} malzeme bulundu ve seçildi. Yanlış olanlara dokunup çıkarabilirsiniz.` : "Fotoğrafta tanıdık bir malzeme bulamadık. Aşağıdan seçebilirsiniz."}
          </p>
        )}
        {demo && (
          <p className="text-sm bg-amber-50 border border-amber-300 text-amber-800 rounded-lg p-3 mt-3">
            ⚠️ <b>Demo modu:</b> fotoğraf gerçekten incelenmedi, örnek malzemeler eklendi. Gerçek tanıma için backend'de
            <code className="mx-1">VISION_PROVIDER=claude</code>ve bir API anahtarı ayarlanmalı.
          </p>
        )}
        {error && <p className="text-sm bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 mt-3">{error}</p>}
      </section>

      <section className="bg-white p-5 rounded-2xl shadow-sm">
        <div className="flex items-center mb-2">
          <h2 className="font-semibold flex-1">Seçili malzemeler ({selected.size})</h2>
          {selected.size > 0 && <button onClick={() => { setSelected(new Set()); setUnsure([]); }} className="text-sm text-slate-500 underline">Temizle</button>}
        </div>
        <div className="flex flex-wrap gap-2 min-h-8">
          {selected.size === 0 && <span className="text-sm text-slate-400">Henüz seçilmedi.</span>}
          {[...selected].map((i) => <Tag key={i} label={i} selected onClick={() => toggle(i)} />)}
        </div>
      </section>

      <section className="bg-white p-5 rounded-2xl shadow-sm">
        <IngredientPicker common={common} unsure={unsure} selected={selected} onToggle={toggle} />
      </section>

      <div className="fixed bottom-0 inset-x-0 bg-gradient-to-t from-slate-50 via-slate-50 to-transparent pt-6 pb-4 px-4">
        <button onClick={findRecipes} disabled={selected.size === 0} className="block w-full max-w-4xl mx-auto bg-emerald-600 text-white rounded-xl py-3.5 text-lg font-semibold shadow-lg disabled:opacity-40 active:bg-emerald-700">
          {selected.size === 0 ? "Malzeme seçin" : `${selected.size} malzemeyle tarif bul`}
        </button>
      </div>
    </div>
  );
}
