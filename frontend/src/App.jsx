import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import MarketplacePage from './pages/MarketplacePage';
import ListingDetailPage from './pages/ListingDetailPage';
import CreateListingWizard from './pages/CreateListingWizard';
import SellerDashboard from './pages/SellerDashboard';
import BuyerDashboard from './pages/BuyerDashboard';
import AdminDashboard from './pages/AdminDashboard';
import ModelEvaluationPage from './pages/ModelEvaluationPage';
import { LoginPage, RegisterPage } from './pages/AuthPages';

export default function App() {
  const [currentRoute, setCurrentRoute] = useState('landing');
  const [selectedListingId, setSelectedListingId] = useState(null);

  const handleNavigate = (route) => {
    setCurrentRoute(route);
    window.scrollTo(0, 0);
  };

  const handleSelectListing = (id) => {
    setSelectedListingId(id);
    setCurrentRoute('detail');
    window.scrollTo(0, 0);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans selection:bg-emerald-500 selection:text-white">
      <Navbar currentRoute={currentRoute} onNavigate={handleNavigate} />

      <main className="flex-1">
        {currentRoute === 'landing' && (
          <LandingPage onNavigate={handleNavigate} />
        )}

        {currentRoute === 'marketplace' && (
          <MarketplacePage onSelectListing={handleSelectListing} />
        )}

        {currentRoute === 'detail' && selectedListingId && (
          <ListingDetailPage
            listingId={selectedListingId}
            onBack={() => setCurrentRoute('marketplace')}
            onNavigate={handleNavigate}
          />
        )}

        {currentRoute === 'wizard' && (
          <CreateListingWizard onNavigate={handleNavigate} />
        )}

        {currentRoute === 'seller-dashboard' && (
          <SellerDashboard onNavigate={handleNavigate} />
        )}

        {currentRoute === 'buyer-dashboard' && (
          <BuyerDashboard onSelectListing={handleSelectListing} onNavigate={handleNavigate} />
        )}

        {currentRoute === 'admin-dashboard' && (
          <AdminDashboard onSelectListing={handleSelectListing} />
        )}

        {currentRoute === 'evaluation' && (
          <ModelEvaluationPage />
        )}

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
