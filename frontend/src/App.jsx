import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import AssessmentPage from './pages/AssessmentPage';
import MarketplacePage from './pages/MarketplacePage';
import ListingDetailPage from './pages/ListingDetailPage';
import CreateListingWizard from './pages/CreateListingWizard';
import ProfilePage from './pages/ProfilePage';
import SellerDashboard from './pages/SellerDashboard';
import BuyerDashboard from './pages/BuyerDashboard';
import AdminDashboard from './pages/AdminDashboard';
import ModelEvaluationPage from './pages/ModelEvaluationPage';
import { LoginPage, RegisterPage } from './pages/AuthPages';

// Path to Route mapper
const getRouteFromPath = (path) => {
  const p = path.toLowerCase().replace(/^\/+|\/+$/g, '');
  if (!p || p === '') return 'landing';
  if (p === 'assessment' || p === 'diagnostics') return 'assessment';
  if (p === 'marketplace' || p === 'catalog') return 'marketplace';
  if (p === 'sell' || p === 'wizard') return 'sell';
  if (p === 'buy' || p === 'orders') return 'buy';
  if (p === 'profile' || p === 'dashboard') return 'profile';
  if (p === 'seller-dashboard') return 'seller-dashboard';
  if (p === 'buyer-dashboard') return 'buyer-dashboard';
  if (p === 'admin-dashboard' || p === 'admin') return 'admin-dashboard';
  if (p === 'evaluation' || p === 'metrics') return 'evaluation';
  if (p === 'login' || p === 'signin') return 'login';
  if (p === 'register' || p === 'signup') return 'register';
  if (p.startsWith('detail/') || p.startsWith('marketplace/')) return 'detail';
  return 'landing';
};

export default function App() {
  const [currentRoute, setCurrentRoute] = useState(() => {
    return getRouteFromPath(window.location.pathname);
  });
  const [selectedListingId, setSelectedListingId] = useState(null);
  const [prefilledAssessmentData, setPrefilledAssessmentData] = useState(null);

  // Sync browser back/forward buttons
  useEffect(() => {
    const handlePopState = () => {
      setCurrentRoute(getRouteFromPath(window.location.pathname));
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const handleNavigate = (route) => {
    setCurrentRoute(route);
    const newPath = route === 'landing' ? '/' : `/${route}`;
    if (window.location.pathname !== newPath) {
      window.history.pushState({}, '', newPath);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectListing = (id) => {
    setSelectedListingId(id);
    setCurrentRoute('detail');
    window.history.pushState({}, '', `/marketplace/${id}`);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleStartListingWithAssessment = (data) => {
    setPrefilledAssessmentData(data);
    handleNavigate('sell');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans selection:bg-emerald-500 selection:text-white">
      <Navbar currentRoute={currentRoute} onNavigate={handleNavigate} />

      <main className="flex-1">
        {/* Route: Home */}
        {currentRoute === 'landing' && (
          <LandingPage onNavigate={handleNavigate} />
        )}

        {/* Route: AI Material Assessment (Dedicated Page 1) */}
        {currentRoute === 'assessment' && (
          <AssessmentPage
            onNavigate={handleNavigate}
            onStartListingWithData={handleStartListingWithAssessment}
          />
        )}

        {/* Route: Construction Waste Marketplace (Dedicated Page 2) */}
        {currentRoute === 'marketplace' && (
          <MarketplacePage onSelectListing={handleSelectListing} />
        )}

        {/* Route: Listing Detail */}
        {currentRoute === 'detail' && selectedListingId && (
          <ListingDetailPage
            listingId={selectedListingId}
            onBack={() => handleNavigate('marketplace')}
            onNavigate={handleNavigate}
          />
        )}

        {/* Route: Sell / Listing Wizard */}
        {(currentRoute === 'sell' || currentRoute === 'wizard') && (
          <CreateListingWizard
            onNavigate={handleNavigate}
            initialData={prefilledAssessmentData}
          />
        )}

        {/* Route: Buy Materials Hub */}
        {currentRoute === 'buy' && (
          <BuyerDashboard
            onSelectListing={handleSelectListing}
            onNavigate={handleNavigate}
          />
        )}

        {/* Route: User Profile Hub */}
        {currentRoute === 'profile' && (
          <ProfilePage
            onNavigate={handleNavigate}
            onSelectListing={handleSelectListing}
          />
        )}

        {/* Sub-Dashboards */}
        {currentRoute === 'seller-dashboard' && (
          <SellerDashboard onNavigate={handleNavigate} />
        )}

        {currentRoute === 'buyer-dashboard' && (
          <BuyerDashboard
            onSelectListing={handleSelectListing}
            onNavigate={handleNavigate}
          />
        )}

        {currentRoute === 'admin-dashboard' && (
          <AdminDashboard onSelectListing={handleSelectListing} />
        )}

        {/* Model Metrics */}
        {currentRoute === 'evaluation' && (
          <ModelEvaluationPage />
        )}

        {/* Authentication */}
        {currentRoute === 'login' && (
          <LoginPage onNavigate={handleNavigate} />
        )}

        {currentRoute === 'register' && (
          <RegisterPage onNavigate={handleNavigate} />
        )}
      </main>

      <Footer onNavigate={handleNavigate} />
    </div>
  );
}
