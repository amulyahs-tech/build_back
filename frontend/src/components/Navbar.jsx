import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Recycle, PlusCircle, ShoppingBag, BarChart3, Shield, LogIn, LogOut, User as UserIcon, Menu, X, Leaf
} from 'lucide-react';

export default function Navbar({ currentRoute, onNavigate }) {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleNav = (route) => {
    onNavigate(route);
    setMobileMenuOpen(false);
  };

  return (
    <nav className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Brand Logo */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => handleNav('landing')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-500/20">
              <Recycle className="w-6 h-6" />
            </div>
            <div>
              <span className="font-bold text-xl tracking-tight text-gray-900">REBUILD <span className="text-emerald-600">AI</span></span>
              <span className="block text-[10px] uppercase tracking-wider font-semibold text-emerald-700">Circular Construction</span>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center gap-1 lg:gap-2">
            <button
              onClick={() => handleNav('marketplace')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${currentRoute === 'marketplace' ? 'bg-emerald-50 text-emerald-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}`}
            >
              <span className="flex items-center gap-1.5">
                <ShoppingBag className="w-4 h-4" />
                Marketplace
              </span>
            </button>

            <button
              onClick={() => handleNav('wizard')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${currentRoute === 'wizard' ? 'bg-emerald-50 text-emerald-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}`}
            >
              <span className="flex items-center gap-1.5">
                <PlusCircle className="w-4 h-4 text-emerald-600" />
                Sell Material (AI Wizard)
              </span>
            </button>

            <button
              onClick={() => handleNav('evaluation')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${currentRoute === 'evaluation' ? 'bg-emerald-50 text-emerald-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}`}
            >
              <span className="flex items-center gap-1.5">
                <BarChart3 className="w-4 h-4" />
                AI Model Metrics
              </span>
            </button>

            {user && (user.user_type === 'SELLER' || user.user_type === 'BOTH') && (
              <button
                onClick={() => handleNav('seller-dashboard')}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition ${currentRoute === 'seller-dashboard' ? 'bg-emerald-50 text-emerald-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}`}
              >
                Seller Hub
              </button>
            )}

            {user && (user.user_type === 'BUYER' || user.user_type === 'BOTH') && (
              <button
                onClick={() => handleNav('buyer-dashboard')}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition ${currentRoute === 'buyer-dashboard' ? 'bg-emerald-50 text-emerald-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}`}
              >
                My Orders
              </button>
            )}

            {user && user.user_type === 'ADMIN' && (
              <button
                onClick={() => handleNav('admin-dashboard')}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition ${currentRoute === 'admin-dashboard' ? 'bg-purple-50 text-purple-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}`}
              >
                <span className="flex items-center gap-1.5">
                  <Shield className="w-4 h-4 text-purple-600" />
                  Admin
                </span>
              </button>
            )}
          </div>

          {/* User Auth Section */}
          <div className="hidden md:flex items-center gap-3">
            {user ? (
              <div className="flex items-center gap-3">
                <div className="flex flex-col text-right">
                  <span className="text-xs font-semibold text-gray-900">{user.name}</span>
                  <span className="text-[10px] text-emerald-600 font-medium capitalize">{user.user_type.toLowerCase()}</span>
                </div>
                <button
                  onClick={logout}
                  title="Log out"
                  className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleNav('login')}
                  className="px-3.5 py-1.5 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition"
                >
                  Sign In
                </button>
                <button
                  onClick={() => handleNav('register')}
                  className="px-4 py-1.5 text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm transition"
                >
                  Get Started
                </button>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden px-4 pt-2 pb-6 space-y-2 border-t border-gray-100 bg-white">
          <button
            onClick={() => handleNav('marketplace')}
            className="w-full text-left px-3 py-2 rounded-lg text-base font-medium text-gray-800 hover:bg-gray-50"
          >
            Marketplace
          </button>
          <button
            onClick={() => handleNav('wizard')}
            className="w-full text-left px-3 py-2 rounded-lg text-base font-medium text-emerald-600 hover:bg-emerald-50"
          >
            Sell Material (AI Wizard)
          </button>
          <button
            onClick={() => handleNav('evaluation')}
            className="w-full text-left px-3 py-2 rounded-lg text-base font-medium text-gray-800 hover:bg-gray-50"
          >
            AI Model Metrics
          </button>
          {user && (
            <>
              <button
                onClick={() => handleNav(user.user_type === 'ADMIN' ? 'admin-dashboard' : 'seller-dashboard')}
                className="w-full text-left px-3 py-2 rounded-lg text-base font-medium text-gray-800 hover:bg-gray-50"
              >
                Dashboard
              </button>
              <button
                onClick={logout}
                className="w-full text-left px-3 py-2 rounded-lg text-base font-medium text-red-600 hover:bg-red-50"
              >
                Sign Out
              </button>
            </>
          )}
          {!user && (
            <div className="pt-2 flex flex-col gap-2">
              <button
                onClick={() => handleNav('login')}
                className="w-full py-2 text-center text-sm font-medium text-gray-700 bg-gray-100 rounded-lg"
              >
                Sign In
              </button>
              <button
                onClick={() => handleNav('register')}
                className="w-full py-2 text-center text-sm font-semibold text-white bg-emerald-600 rounded-lg"
              >
                Register
              </button>
            </div>
          )}
        </div>
      )}
    </nav>
  );
}
