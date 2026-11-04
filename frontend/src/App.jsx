import { Link, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { auth } from "./api.js";
import LoginPage from "./pages/LoginPage.jsx";
import AnalyzePage from "./pages/AnalyzePage.jsx";
import ResultsPage from "./pages/ResultsPage.jsx";
import RecipePage from "./pages/RecipePage.jsx";
import FavoritesPage from "./pages/FavoritesPage.jsx";

function RequireLogin({ children }) {
  return auth.token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  const navigate = useNavigate();
  const logout = () => { auth.set(null); navigate("/login"); };
  return (
    <div className="min-h-screen">
      <header className="bg-white border-b">
        <nav className="max-w-4xl mx-auto px-4 py-3 flex items-center gap-4">
          <Link to="/" className="font-bold text-emerald-600 text-lg">SnapFridge</Link>
          {auth.token && (
            <>
              <Link to="/" className="text-sm hover:underline">Malzemeler</Link>
              <Link to="/favorites" className="text-sm hover:underline">Favoriler</Link>
              <button onClick={logout} className="ml-auto text-sm text-slate-500 hover:underline">Çıkış</button>
            </>
          )}
        </nav>
      </header>
      <main className="max-w-4xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<RequireLogin><AnalyzePage /></RequireLogin>} />
          <Route path="/results" element={<RequireLogin><ResultsPage /></RequireLogin>} />
          <Route path="/recipes/:id" element={<RequireLogin><RecipePage /></RequireLogin>} />
          <Route path="/favorites" element={<RequireLogin><FavoritesPage /></RequireLogin>} />
          {/* TODO (İdil, WBS-6.1): /admin tarif yönetimi sayfası */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
