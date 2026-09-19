import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  User as UserIcon, Mail, Phone, MapPin, Building, ShieldCheck,
  ShoppingBag, PlusCircle, Leaf, LogOut, CheckCircle2, Package, Clock
} from 'lucide-react';
import SellerDashboard from './SellerDashboard';
import BuyerDashboard from './BuyerDashboard';
import AdminDashboard from './AdminDashboard';

export default function ProfilePage({ onNavigate, onSelectListing }) {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('overview'); // 'overview', 'seller', 'buyer', 'admin'

  if (!user) {
    return (
      <div className="max-w-md mx-auto my-16 px-4">
        <div className="bg-white rounded-3xl p-8 border border-gray-200 shadow-xl text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto">
            <UserIcon className="w-8 h-8" />
          </div>
          <h2 className="text-xl font-bold text-gray-900">Sign in to BuildBack</h2>
          <p className="text-xs text-gray-500">
            Access your active listings, purchase requests, AI diagnostics history, and circular carbon impact metrics.
          </p>
          <div className="space-y-2 pt-2">
            <button
              onClick={() => onNavigate('login')}
              className="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold rounded-xl shadow transition"
            >
              Log In to Account
            </button>
            <button
              onClick={() => onNavigate('register')}
              className="w-full py-2.5 px-4 bg-gray-50 hover:bg-gray-100 text-gray-700 text-sm font-semibold rounded-xl border border-gray-200 transition"
            >
              Create Free Account
            </button>
          </div>
        </div>
      </div>
    );
  }

  const isSeller = user.user_type === 'SELLER' || user.user_type === 'BOTH';
  const isBuyer = user.user_type === 'BUYER' || user.user_type === 'BOTH';
  const isAdmin = user.user_type === 'ADMIN';

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Profile Header Banner */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div className="flex items-center gap-5">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white font-black text-2xl flex items-center justify-center shadow-lg shadow-emerald-600/20 flex-shrink-0">
            {user.name?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-black text-gray-900">{user.name}</h1>
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider ${
                isAdmin ? 'bg-purple-100 text-purple-800' :
                isSeller ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-100 text-blue-800'
              }`}>
                {user.user_type}
              </span>
            </div>
            <p className="text-xs text-gray-500 flex items-center gap-3 mt-1">
              <span className="flex items-center gap-1"><Mail className="w-3.5 h-3.5" /> {user.email}</span>
              {user.company_name && (
                <span className="flex items-center gap-1"><Building className="w-3.5 h-3.5" /> {user.company_name}</span>
              )}
              {user.city && (
                <span className="flex items-center gap-1"><MapPin className="w-3.5 h-3.5" /> {user.city}, {user.state}</span>
              )}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          {isSeller && (
            <button
              onClick={() => onNavigate('sell')}
              className="flex-1 sm:flex-initial px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-xl shadow transition flex items-center justify-center gap-1.5"
            >
              <PlusCircle className="w-4 h-4" />
              List Material
            </button>
          )}
          <button
            onClick={logout}
            className="flex-1 sm:flex-initial px-4 py-2 bg-gray-100 hover:bg-red-50 hover:text-red-700 text-gray-700 text-xs font-semibold rounded-xl transition flex items-center justify-center gap-1.5"
          >
            <LogOut className="w-4 h-4" />
            Log Out
          </button>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="flex border-b border-gray-200 gap-3 overflow-x-auto">
        <button
          onClick={() => setActiveTab('overview')}
          className={`py-3 px-4 text-xs font-semibold flex items-center gap-2 border-b-2 transition whitespace-nowrap ${
            activeTab === 'overview'
              ? 'border-emerald-600 text-emerald-700 bg-emerald-50/40 rounded-t-lg'
              : 'border-transparent text-gray-500 hover:text-gray-900'
          }`}
        >
          <ShieldCheck className="w-4 h-4" />
          Profile Overview & Impact
        </button>

        {isSeller && (
          <button
            onClick={() => setActiveTab('seller')}
            className={`py-3 px-4 text-xs font-semibold flex items-center gap-2 border-b-2 transition whitespace-nowrap ${
              activeTab === 'seller'
                ? 'border-emerald-600 text-emerald-700 bg-emerald-50/40 rounded-t-lg'
                : 'border-transparent text-gray-500 hover:text-gray-900'
            }`}
          >
            <Package className="w-4 h-4" />
            Seller Inventory & Offers
          </button>
        )}

        {isBuyer && (
          <button
            onClick={() => setActiveTab('buyer')}
            className={`py-3 px-4 text-xs font-semibold flex items-center gap-2 border-b-2 transition whitespace-nowrap ${
              activeTab === 'buyer'
                ? 'border-emerald-600 text-emerald-700 bg-emerald-50/40 rounded-t-lg'
                : 'border-transparent text-gray-500 hover:text-gray-900'
            }`}
          >
            <ShoppingBag className="w-4 h-4" />
            My Orders & Requests
          </button>
        )}

        {isAdmin && (
          <button
            onClick={() => setActiveTab('admin')}
            className={`py-3 px-4 text-xs font-semibold flex items-center gap-2 border-b-2 transition whitespace-nowrap ${
              activeTab === 'admin'
                ? 'border-purple-600 text-purple-700 bg-purple-50/40 rounded-t-lg'
                : 'border-transparent text-gray-500 hover:text-gray-900'
            }`}
          >
            <ShieldCheck className="w-4 h-4 text-purple-600" />
            Admin Platform Control
          </button>
        )}
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Circular ESG Credentials */}
          <div className="bg-gradient-to-br from-emerald-800 to-teal-900 text-white rounded-3xl p-6 shadow-lg space-y-4">
            <div className="flex items-center gap-2 text-emerald-300 text-xs font-semibold uppercase tracking-wider">
              <Leaf className="w-4 h-4" />
              Circular ESG Footprint
            </div>
            <h3 className="text-xl font-bold">Lifetime Sustainability Contribution</h3>
            <div className="space-y-3 pt-2">
              <div className="bg-white/10 p-3 rounded-xl backdrop-blur-sm">
                <span className="block text-xs text-emerald-200">Avoided Embodied Carbon</span>
                <span className="text-2xl font-black">2,450 kg CO2e</span>
              </div>
              <div className="bg-white/10 p-3 rounded-xl backdrop-blur-sm">
                <span className="block text-xs text-emerald-200">Landfill Waste Diverted</span>
                <span className="text-2xl font-black">14.8 Metric Tonnes</span>
              </div>
              <div className="bg-white/10 p-3 rounded-xl backdrop-blur-sm">
                <span className="block text-xs text-emerald-200">Mature Tree Offset</span>
                <span className="text-2xl font-black">112 Trees / Year</span>
              </div>
            </div>
          </div>

          {/* Account Details Card */}
          <div className="lg:col-span-2 bg-white rounded-3xl p-6 border border-gray-200 shadow-sm space-y-6">
            <h3 className="text-base font-bold text-gray-900">Account Credentials & Verification</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div className="p-3.5 bg-gray-50 rounded-xl border border-gray-200">
                <span className="text-gray-400 block mb-0.5">Full Name</span>
                <span className="font-semibold text-gray-900 text-sm">{user.name}</span>
              </div>
              <div className="p-3.5 bg-gray-50 rounded-xl border border-gray-200">
                <span className="text-gray-400 block mb-0.5">Email Address</span>
                <span className="font-semibold text-gray-900 text-sm">{user.email}</span>
              </div>
              <div className="p-3.5 bg-gray-50 rounded-xl border border-gray-200">
                <span className="text-gray-400 block mb-0.5">Organization / Company</span>
                <span className="font-semibold text-gray-900 text-sm">{user.company_name || "Individual Operator"}</span>
              </div>
              <div className="p-3.5 bg-gray-50 rounded-xl border border-gray-200">
                <span className="text-gray-400 block mb-0.5">Operating Region</span>
                <span className="font-semibold text-gray-900 text-sm">{user.city || "Bangalore"}, {user.state || "Karnataka"}</span>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-100 flex items-center justify-between">
              <span className="text-xs text-emerald-600 font-semibold flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                Verified Circular Partner
              </span>
              <button
                onClick={() => onNavigate('assessment')}
                className="text-xs font-semibold text-gray-700 hover:text-emerald-700 underline"
              >
                Run New AI Assessment &rarr;
              </button>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'seller' && (
        <SellerDashboard onNavigate={onNavigate} />
      )}

      {activeTab === 'buyer' && (
        <BuyerDashboard onSelectListing={onSelectListing} onNavigate={onNavigate} />
      )}

      {activeTab === 'admin' && (
        <AdminDashboard onSelectListing={onSelectListing} />
      )}
    </div>
  );
}
