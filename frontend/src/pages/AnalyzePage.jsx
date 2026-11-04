// Ana akış: fotoğraf yükle (isteğe bağlı) → malzemeleri düzelt → tarif bul.
// Sahibi: Ahmet İlker (WBS-4.2), entegrasyon: Biray (WBS-5.1).
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api.js";
import IngredientPicker from "../components/IngredientPicker.jsx";
import Tag from "../components/Tag.jsx";

export default function AnalyzePage() {
  const [common, setCommon] = useState([]);
  const [unsure, setUnsure] = useState([]);
  const [selected, setSelected] = useState(new Set());
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => { api.commonIngredients().then(setCommon).catch((e) => setError(e.message)); }, []);

  const toggle = (name) => setSelected((prev) => {
    const next = new Set(prev);
    next.has(name) ? next.delete(name) : next.add(name);
    return next;
  });

  const onPhoto = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setError(""); setBusy(true);
    try {
      const res = await api.recognize(file);
      setSelected((prev) => new Set([...prev, ...res.sure]));
      setUnsure(res.unsure);
    } catch (err) {
      setError(err.message + " Malzemeleri aşağıdan elle seçebilirsiniz.");
    } finally { setBusy(false); e.target.value = ""; }
  };

  const findRecipes = () => navigate("/results", { state: { ingredients: [...selected] } });

  return (
    <div className="space-y-6">
      <section className="bg-white p-5 rounded-xl shadow">
        <h1 className="text-xl font-bold mb-1">Buzdolabında ne var?</h1>
        <p className="text-sm text-slate-500 mb-3">Fotoğraf yükleyin ya da bu adımı atlayıp malzemeleri kendiniz seçin.</p>
        <label className="inline-block bg-emerald-600 text-white px-4 py-2 rounded-lg cursor-pointer">
          {busy ? "Fotoğraf inceleniyor…" : "📷 Fotoğraf yükle (JPEG/PNG, en çok 10 MB)"}
          <input type="file" accept="image/jpeg,image/png" className="hidden" onChange={onPhoto} disabled={busy} />
        </label>
        {error && <p className="text-red-600 text-sm mt-3">{error}</p>}
      </section>

      <section className="bg-white p-5 rounded-xl shadow">
        <h2 className="font-semibold mb-2">Seçili malzemeler ({selected.size})</h2>
        <div className="flex flex-wrap gap-2 min-h-8">
          {selected.size === 0 && <span className="text-sm text-slate-400">Henüz seçilmedi.</span>}
          {[...selected].map((i) => <Tag key={i} label={i} selected onClick={() => toggle(i)} />)}
        </div>
      </section>

      <section className="bg-white p-5 rounded-xl shadow">
        <IngredientPicker common={common} unsure={unsure} selected={selected} onToggle={toggle} />
      </section>

      <button onClick={findRecipes} disabled={selected.size === 0} className="w-full bg-emerald-600 text-white rounded-lg py-3 text-lg disabled:opacity-40">
        Tarif bul
      </button>
    </div>
  );
}
