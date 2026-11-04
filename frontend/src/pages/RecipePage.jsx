// Tarif detayı + favori. Sahibi: Ahmet İlker (arayüz), Umut (favoriler, WBS-5.2).
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api.js";

export default function RecipePage() {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [isFav, setIsFav] = useState(false);
  const [error, setError] = useState("");

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
  if (!recipe) return <p>Yükleniyor…</p>;
  return (
    <article className="bg-white p-6 rounded-xl shadow space-y-4">
      <div className="flex items-start gap-4">
        <h1 className="text-2xl font-bold flex-1">{recipe.title}</h1>
        <button onClick={toggleFav} className="border rounded-lg px-3 py-1">{isFav ? "★ Favoride" : "☆ Favorilere ekle"}</button>
      </div>
      {recipe.image_url && <img src={recipe.image_url} alt="" className="w-full max-h-72 object-cover rounded-lg" />}
      <ul className="list-disc pl-6">
        {recipe.ingredients.map((i) => <li key={i.name}>{i.measure} {i.name}</li>)}
      </ul>
      <p className="whitespace-pre-line">{recipe.instructions}</p>
    </article>
  );
}
