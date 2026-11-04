// Tarif detayı + favori. Sahibi: Ahmet İlker (arayüz), Umut (favoriler, WBS-5.2).
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api.js";
import { tr } from "../labels.js";
import { loadSelection } from "../selection.js";

const STAPLES = new Set(["salt", "water", "black pepper", "oil", "vegetable oil"]);

// Tarif metnini adımlara böler (veri setinde adımlar satır satır ya da "STEP 1" diye yazılı).
function steps(text) {
  return text
    .split(/\r?\n|(?=STEP \d+)/i)
    .map((s) => s.replace(/^\s*(step\s*\d+[:.)]?|\d+[.)])\s*/i, "").trim())
    .filter((s) => s.length > 2);
}

export default function RecipePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState(null);
  const [isFav, setIsFav] = useState(false);
  const [error, setError] = useState("");
  const have = new Set(loadSelection());

  useEffect(() => {
    api.recipe(id).then(setRecipe).catch((e) => setError(e.message));
    api.favorites().then((f) => setIsFav(f.some((r) => String(r.id) === id))).catch(() => {});
  }, [id]);

  const toggleFav = async () => {
    try {
      isFav ? await api.removeFavorite(id) : await api.addFavorite(id);
      setIsFav(!isFav);
    } catch (e) { setError(e.message); }
  };

  if (error) return <p className="text-red-600">{error}</p>;
  if (!recipe) return <p className="text-slate-500">Yükleniyor…</p>;
  return (
    <article className="bg-white rounded-2xl shadow-sm overflow-hidden">
      {recipe.image_url && <img src={recipe.image_url} alt="" className="w-full h-56 sm:h-72 object-cover" />}
      <div className="p-5 space-y-5">
        <button onClick={() => navigate(-1)} className="text-emerald-700 text-sm">← Geri</button>
        <div className="flex items-start gap-3">
          <h1 className="text-2xl font-bold flex-1 leading-tight">{recipe.title}</h1>
          <button onClick={toggleFav} className={`border rounded-xl px-3 py-1.5 text-sm whitespace-nowrap ${isFav ? "bg-amber-50 border-amber-300" : ""}`}>
            {isFav ? "★ Favoride" : "☆ Favorile"}
          </button>
        </div>

        <section>
          <h2 className="font-semibold mb-2">Malzemeler</h2>
          <ul className="divide-y">
            {recipe.ingredients.map((i) => {
              const ok = have.has(i.name) || STAPLES.has(i.name);
              return (
                <li key={i.name} className="flex items-center gap-3 py-2">
                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${ok ? "bg-emerald-100 text-emerald-700" : "bg-red-50 text-red-500"}`}>{ok ? "✓" : "✗"}</span>
                  <span className="flex-1">
                    {tr(i.name) !== i.name ? tr(i.name) : i.label || i.name}
                    {i.label && tr(i.name) !== i.name && <span className="text-slate-400 text-sm"> ({i.label})</span>}
                  </span>
                  <span className="text-sm text-slate-500 text-right">{i.measure}</span>
                </li>
              );
            })}
          </ul>
        </section>

        <section>
          <h2 className="font-semibold mb-2">Yapılışı</h2>
          <ol className="space-y-3">
            {steps(recipe.instructions).map((s, n) => (
              <li key={n} className="flex gap-3">
                <span className="w-6 h-6 shrink-0 rounded-full bg-emerald-600 text-white text-xs flex items-center justify-center mt-0.5">{n + 1}</span>
                <p className="leading-relaxed">{s}</p>
              </li>
            ))}
          </ol>
        </section>

        {recipe.source === "themealdb" && <p className="text-xs text-slate-400">Kaynak: TheMealDB (themealdb.com)</p>}
      </div>
    </article>
  );
}
