// Giriş / kayıt. Sahibi: Ahmet İlker (arayüz) + Biray (backend).
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api.js";

export default function LoginPage() {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError(""); setBusy(true);
    try {
      if (mode === "register") await api.register(email, password);
      await api.login(email, password);
      navigate("/");
    } catch (err) { setError(err.message); } finally { setBusy(false); }
  };

  return (
    <form onSubmit={submit} className="max-w-sm mx-auto bg-white p-6 rounded-xl shadow space-y-4">
      <h1 className="text-xl font-bold">{mode === "login" ? "Giriş yap" : "Kayıt ol"}</h1>
      <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="E-posta" className="w-full border rounded-lg px-3 py-2" />
      <input type="password" required minLength={6} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Şifre (en az 6)" className="w-full border rounded-lg px-3 py-2" />
      {error && <p className="text-red-600 text-sm">{error}</p>}
      <button disabled={busy} className="w-full bg-emerald-600 text-white rounded-lg py-2 disabled:opacity-50">
        {busy ? "Bekleyin…" : mode === "login" ? "Giriş" : "Kayıt ol"}
      </button>
      <button type="button" onClick={() => setMode(mode === "login" ? "register" : "login")} className="text-sm text-emerald-700 hover:underline">
        {mode === "login" ? "Hesabın yok mu? Kayıt ol" : "Hesabın var mı? Giriş yap"}
      </button>
    </form>
  );
}
