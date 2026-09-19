import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Recycle, Sparkles, ShoppingBag, PlusCircle, User, LogIn, LogOut,
  Shield, Menu, X, BarChart3, ShoppingCart
} from 'lucide-react';

export default function Navbar({ currentRoute, onNavigate }) {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleNav = (route) => {
    onNavigate(route);
    setMobileMenuOpen(false);
  };

  const navLinks = [
    { id: 'landing', label: 'Home' },
    { id: 'assessment', label: 'AI Assessment', highlight: true, icon: Sparkles },
    { id: 'marketplace', label: 'Marketplace', icon: ShoppingBag },
    { id: 'sell', label: 'Sell', icon: PlusCircle },
    { id: 'buy', label: 'Buy', icon: ShoppingCart },
    { id: 'profile', label: 'Profile', icon: User },
  ];

  return (
    <nav className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Brand Logo: BUILD BACK */}
          <div
            className="flex items-center gap-3 cursor-pointer select-none"
            onClick={() => handleNav('landing')}
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-500/20">
              <Recycle className="w-6 h-6" />
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight text-gray-900">
                BUILD<span className="text-emerald-600">BACK</span>
              </span>
              <span className="block text-[10px] uppercase tracking-wider font-bold text-emerald-700">
                AI Circular Waste Platform
              </span>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden lg:flex items-center gap-1 xl:gap-2">
            {navLinks.map((item) => {
              const isActive = currentRoute === item.id || (item.id === 'sell' && currentRoute === 'wizard');
              return (
                <button
                  key={item.id}
                  onClick={() => handleNav(item.id)}
                  className={`px-3 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-1.5 ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-700 shadow-sm'
                      : item.highlight
                      ? 'text-emerald-700 bg-emerald-50/50 hover:bg-emerald-100/60'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100/70'
                  }`}
                >
                  {item.icon && <item.icon className="w-4 h-4 text-emerald-600" />}
                  {item.label}
                </button>
              );
            })}

            {user?.user_type === 'ADMIN' && (
              <button
                onClick={() => handleNav('admin-dashboard')}
                className={`px-3 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-1.5 ${
                  currentRoute === 'admin-dashboard'
                    ? 'bg-purple-50 text-purple-700'
                    : 'text-purple-600 hover:bg-purple-50'
                }`}
              >
                <Shield className="w-4 h-4" />
                Admin
              </button>
            )}
          </div>

          {/* User Auth Section */}
          <div className="hidden md:flex items-center gap-3">
            {user ? (
              <div className="flex items-center gap-3">
                <button
                  onClick={() => handleNav('profile')}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-xl hover:bg-gray-100 transition text-left"
                >
                  <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 font-bold flex items-center justify-center text-xs">
                    {user.name?.charAt(0).toUpperCase() || 'U'}
                  </div>
                  <div className="flex flex-col">
                    <span className="text-xs font-bold text-gray-900 leading-tight">{user.name}</span>
                    <span className="text-[10px] text-emerald-600 font-semibold uppercase tracking-wider">{user.user_type}</span>
                  </div>
                </button>

                <button
                  onClick={logout}
                  title="Sign out"
                  className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleNav('login')}
                  className="px-3.5 py-1.5 text-sm font-semibold text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-xl transition"
                >
                  Login
                </button>
                <button
                  onClick={() => handleNav('register')}
                  className="px-4 py-1.5 text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-sm transition"
                >
                  Register
                </button>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="lg:hidden flex items-center">
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
        <div className="lg:hidden px-4 pt-2 pb-6 space-y-1.5 border-t border-gray-100 bg-white">
          {navLinks.map((item) => (
            <button
              key={item.id}
              onClick={() => handleNav(item.id)}
              className={`w-full text-left px-3.5 py-2.5 rounded-xl text-sm font-semibold flex items-center gap-2.5 ${
                currentRoute === item.id
                  ? 'bg-emerald-50 text-emerald-700'
                  : 'text-gray-800 hover:bg-gray-50'
              }`}
            >
              {item.icon && <item.icon className="w-4 h-4 text-emerald-600" />}
              {item.label}
            </button>
          ))}

          {user?.user_type === 'ADMIN' && (
            <button
              onClick={() => handleNav('admin-dashboard')}
              className="w-full text-left px-3.5 py-2.5 rounded-xl text-sm font-semibold text-purple-700 hover:bg-purple-50 flex items-center gap-2"
            >
              <Shield className="w-4 h-4" />
              Admin Platform
            </button>
          )}

          <div className="pt-2 border-t border-gray-100">
            {user ? (
              <div className="flex items-center justify-between pt-2 px-1">
                <div className="flex flex-col">
                  <span className="text-xs font-bold text-gray-900">{user.name}</span>
                  <span className="text-[10px] text-emerald-600 font-semibold">{user.email}</span>
                </div>
                <button
                  onClick={logout}
                  className="px-3 py-1.5 text-xs font-semibold text-red-600 hover:bg-red-50 rounded-lg"
                >
                  Log Out
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-2 pt-1">
                <button
                  onClick={() => handleNav('login')}
                  className="w-full py-2 text-center text-xs font-bold text-gray-700 bg-gray-100 rounded-xl"
                >
                  Login
                </button>
                <button
                  onClick={() => handleNav('register')}
                  className="w-full py-2 text-center text-xs font-bold text-white bg-emerald-600 rounded-xl"
                >
                  Register
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
