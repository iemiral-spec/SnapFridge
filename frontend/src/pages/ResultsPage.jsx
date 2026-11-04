// Tarif önerileri. Sahibi: Ahmet İlker (arayüz) + İdil (eşleştirme).
import { useEffect, useState } from "react";
import { Link, Navigate, useLocation } from "react-router-dom";
import { api } from "../api.js";

export default function ResultsPage() {
  const ingredients = useLocation().state?.ingredients;
  const [recipes, setRecipes] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (ingredients?.length) api.match(ingredients).then(setRecipes).catch((e) => setError(e.message));
  }, [ingredients]);

  if (!ingredients?.length) return <Navigate to="/" replace />;
  if (error) return <p className="text-red-600">{error}</p>;
  if (recipes === null) return <p>Tarifler aranıyor…</p>;
  if (recipes.length === 0)
    return <p>Bu malzemelerle eşleşen tarif bulamadık. <Link to="/" className="text-emerald-700 underline">Malzeme ekleyin</Link>.</p>;

  return (
    <div className="space-y-3">
      <h1 className="text-xl font-bold">Önerilen tarifler</h1>
      {recipes.map((r) => (
        <Link key={r.id} to={`/recipes/${r.id}`} className="flex gap-4 bg-white p-4 rounded-xl shadow hover:ring-2 ring-emerald-300">
          {r.image_url && <img src={r.image_url} alt="" className="w-20 h-20 object-cover rounded-lg" />}
          <div>
            <h2 className="font-semibold">{r.title}</h2>
            <p className="text-sm text-emerald-700">Var: {r.matched.join(", ")}</p>
            {r.missing.length > 0 && <p className="text-sm text-red-600">Eksik: {r.missing.join(", ")}</p>}
          </div>
        </Link>
      ))}
    </div>
  );
}
