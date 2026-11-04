// Tıklanabilir malzeme etiketi. Ad Türkçe gösterilir, değer İngilizce kalır.
import { tr } from "../labels.js";

export default function Tag({ label, selected, variant = "normal", onClick }) {
  const base = "px-3 py-1.5 rounded-full text-sm border transition active:scale-95";
  const style = selected
    ? "bg-emerald-600 text-white border-emerald-600"
    : variant === "unsure"
      ? "bg-amber-50 text-amber-800 border-amber-300 border-dashed hover:bg-amber-100"
      : "bg-white text-slate-700 border-slate-300 hover:bg-slate-100";
  return (
    <button type="button" onClick={onClick} className={`${base} ${style}`} aria-pressed={selected}>
      {selected ? "✓ " : ""}{tr(label)}
    </button>
  );
}
