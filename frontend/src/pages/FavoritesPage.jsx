// Favori tarifler. Sahibi: Umut (WBS-5.2).
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api.js";

export default function FavoritesPage() {
  const [favs, setFavs] = useState(null);
  useEffect(() => { api.favorites().then(setFavs).catch(() => setFavs([])); }, []);
  if (favs === null) return <p>Yükleniyor…</p>;
  if (favs.length === 0) return <p>Henüz favori tarifiniz yok.</p>;
  return (
    <div className="space-y-2">
      <h1 className="text-xl font-bold">Favorilerim</h1>
      {favs.map((r) => (
        <Link key={r.id} to={`/recipes/${r.id}`} className="block bg-white p-4 rounded-xl shadow hover:underline">{r.title}</Link>
      ))}
    </div>
  );
}
