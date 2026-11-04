// Backend ile konuşan tek yer (API adaptörü). Sahibi: Ahmet İlker (WBS-4.2).
const BASE = import.meta.env.VITE_API_URL || "";

export const auth = {
  get token() { return localStorage.getItem("token"); },
  set(token) { token ? localStorage.setItem("token", token) : localStorage.removeItem("token"); },
};

async function request(path, { method = "GET", json, body, headers = {} } = {}) {
  const h = { ...headers };
  if (auth.token) h.Authorization = `Bearer ${auth.token}`;
  if (json !== undefined) { h["Content-Type"] = "application/json"; body = JSON.stringify(json); }
  const res = await fetch(BASE + path, { method, headers: h, body });
  if (res.status === 401) auth.set(null);
  if (!res.ok) {
    let msg = `Hata (${res.status})`;
    try { const d = await res.json(); if (typeof d.detail === "string") msg = d.detail; } catch { /* boş */ }
    throw new Error(msg);
  }
  return res.status === 204 ? null : res.json();
}

export const api = {
  register: (email, password) => request("/api/auth/register", { method: "POST", json: { email, password } }),
  login: async (email, password) => {
    const form = new URLSearchParams({ username: email, password });
    const data = await request("/api/auth/login", { method: "POST", body: form });
    auth.set(data.access_token);
  },
  me: () => request("/api/auth/me"),
  commonIngredients: () => request("/api/ingredients/common"),
  searchIngredients: (q) => request(`/api/ingredients/search?q=${encodeURIComponent(q)}`),
  recognize: (file) => { const fd = new FormData(); fd.append("photo", file); return request("/api/recognize", { method: "POST", body: fd }); },
  match: (ingredients) => request("/api/recipes/match", { method: "POST", json: { ingredients } }),
  recipe: (id) => request(`/api/recipes/${id}`),
  favorites: () => request("/api/favorites"),
  addFavorite: (id) => request(`/api/favorites/${id}`, { method: "PUT" }),
  removeFavorite: (id) => request(`/api/favorites/${id}`, { method: "DELETE" }),
};
