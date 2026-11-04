// Seçili malzemeler sekme açık kaldığı sürece hatırlanır: geri dönünce seçim kaybolmaz,
// tarif detayında hangi malzemenin elde olduğu gösterilebilir.
const KEY = "snapfridge:selected";

export function loadSelection() {
  try { return JSON.parse(sessionStorage.getItem(KEY)) || []; } catch { return []; }
}

export function saveSelection(items) {
  try { sessionStorage.setItem(KEY, JSON.stringify(items)); } catch { /* gizli sekme vb. */ }
}
