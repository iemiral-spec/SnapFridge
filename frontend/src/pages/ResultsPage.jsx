// Tarif önerileri. Sahibi: Ahmet İlker (arayüz) + İdil (eşleştirme).
import { useEffect, useState } from "react";
import { Link, Navigate, useLocation } from "react-router-dom";
import { api } from "../api.js";
import { tr } from "../labels.js";
import { loadSelection } from "../selection.js";

// TheMealDB görsellerinin küçük boyu var; mobilde daha hızlı yüklenir.
const thumb = (url) => (url.includes("themealdb.com") ? `${url}/small` : url);

const FILTERS = [
  { label: "Tümü", max: Infinity },
  { label: "En çok 2 eksik", max: 2 },
  { label: "Eksiksiz", max: 0 },
];

export default function ResultsPage() {
  const ingredients = useLocation().state?.ingredients ?? loadSelection();
  const [recipes, setRecipes] = useState(null);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState(FILTERS[0]);

  const key = ingredients.join("|");
  useEffect(() => {
    if (ingredients.length) api.match(ingredients).then(setRecipes).catch((e) => setError(e.message));
  }, [key]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!ingredients.length) return <Navigate to="/" replace />;
  if (error) return <p className="text-red-600">{error}</p>;
  if (recipes === null) return <p className="text-slate-500">Tarifler aranıyor…</p>;
  if (recipes.length === 0)
    return <p>Bu malzemelerle eşleşen tarif bulamadık. <Link to="/" className="text-emerald-700 underline">Malzeme ekleyin</Link>.</p>;

  const shown = recipes.filter((r) => r.missing.length <= filter.max);
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <Link to="/" className="text-emerald-700 text-sm">← Malzemeler</Link>
        <h1 className="text-xl font-bold">Önerilen tarifler</h1>
      </div>
      <div className="flex gap-2 overflow-x-auto pb-1">
        {FILTERS.map((f) => (
          <button key={f.label} onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-full text-sm border whitespace-nowrap ${f === filter ? "bg-slate-800 text-white border-slate-800" : "bg-white border-slate-300"}`}>
            {f.label} ({recipes.filter((r) => r.missing.length <= f.max).length})
          </button>
        ))}
      </div>
      {shown.length === 0 && <p className="text-slate-500 text-sm">Bu filtrede tarif yok.</p>}
      {shown.map((r) => (
        <Link key={r.id} to={`/recipes/${r.id}`} className="flex gap-3 bg-white p-3 rounded-2xl shadow-sm active:ring-2 hover:ring-2 ring-emerald-300">
          {r.image_url
            ? <img src={thumb(r.image_url)} alt="" loading="lazy" className="w-24 h-24 object-cover rounded-xl shrink-0" />
            : <div className="w-24 h-24 rounded-xl bg-emerald-50 flex items-center justify-center text-3xl shrink-0">🍳</div>}
          <div className="min-w-0 flex-1">
            <h2 className="font-semibold leading-tight">{r.title}</h2>
            <div className="flex items-center gap-2 mt-1.5">
              <div className="h-1.5 flex-1 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500" style={{ width: `${Math.round(r.score * 100)}%` }} />
              </div>
              <span className="text-xs text-slate-500">{r.matched.length}/{r.matched.length + r.missing.length}</span>
            </div>
            <p className="text-sm text-emerald-700 mt-1 line-clamp-1">✓ {r.matched.map(tr).join(", ")}</p>
            {r.missing.length > 0
              ? <p className="text-sm text-red-600 line-clamp-2">Eksik: {r.missing.map(tr).join(", ")}</p>
              : <p className="text-sm text-emerald-700 font-medium">Hepsi var!</p>}
          </div>
        </Link>
      ))}
    </div>
  );
}
