// frontend/src/App.tsx
import { Suspense, lazy } from 'react';
import { BrowserRouter, useLocation } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import AppRoutes from './routes/AppRoutes';
import tuitImage from './pages/tuit.jpg';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './i18n';

const NewHeader = lazy(() => import('./components/Headers/NewHeader'));
const Footer = lazy(() => import('./components/Footer/Footer'));

const LoadingSpinner = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
);

const Layout = () => {
  const location = useLocation();

  // страницы без header/footer
  const hideLayout = ['/login', '/register'].includes(location.pathname);

  return (
    <>
      <div className="relative w-full min-w-max z-10 min-h-screen flex flex-col">
        {/* Фон */}
        <div
          className="absolute inset-0 w-full h-full -z-20 bg-cover bg-center bg-fixed"
          style={{ backgroundImage: `url(${tuitImage})` }}
        />

        {/* Overlay */}
        <div className="absolute inset-0 w-full h-full -z-10 bg-[rgba(0,20,50,0.55)] backdrop-blur-md" />

        {/* Контент */}
        <Suspense fallback={<LoadingSpinner />}>
          {!hideLayout && <NewHeader />}
          <AppRoutes />
          {!hideLayout && <Footer />}
        </Suspense>
      </div>
    </>
  );
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Layout />
        <ToastContainer position="top-right" autoClose={3000} />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
