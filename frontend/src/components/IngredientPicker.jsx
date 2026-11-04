// Malzeme seçim ekranı: "emin değil" bölümü, ortak etiketler ve arama kutusu.
// Sahibi: Ahmet İlker (WBS-4.2).
import { useEffect, useState } from "react";
import { api } from "../api.js";
import Tag from "./Tag.jsx";

export default function IngredientPicker({ common, unsure, selected, onToggle }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    const q = query.trim();
    if (!q) { setResults([]); return; }
    const t = setTimeout(() => api.searchIngredients(q).then(setResults).catch(() => setResults([])), 250);
    return () => clearTimeout(t);
  }, [query]);

  return (
    <div className="space-y-5">
      {unsure.length > 0 && (
        <section>
          <h3 className="font-semibold text-amber-700 mb-2">Emin değiliz, var mı? (tıklayıp ekleyin)</h3>
          <div className="flex flex-wrap gap-2">
            {unsure.map((i) => <Tag key={i} label={i} variant="unsure" selected={selected.has(i)} onClick={() => onToggle(i)} />)}
          </div>
        </section>
      )}
      <section>
        <h3 className="font-semibold mb-2">Sık kullanılan malzemeler</h3>
        <div className="flex flex-wrap gap-2">
          {common.map((i) => <Tag key={i} label={i} selected={selected.has(i)} onClick={() => onToggle(i)} />)}
        </div>
      </section>
      <section>
        <h3 className="font-semibold mb-2">Listede yok mu? Arayın</h3>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="ör. yoğurt → yogurt"
          className="w-full border rounded-lg px-3 py-2"
        />
        <div className="flex flex-wrap gap-2 mt-2">
          {results.map((i) => <Tag key={i} label={i} selected={selected.has(i)} onClick={() => onToggle(i)} />)}
        </div>
      </section>
    </div>
  );
}
