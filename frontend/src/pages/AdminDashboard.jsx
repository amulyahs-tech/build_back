import React, { useState, useEffect } from 'react';
import {
  Shield, Users, Layers, TrendingUp, AlertTriangle, CheckCircle, Flag, RefreshCw
} from 'lucide-react';
import { api } from '../services/api';

export default function AdminDashboard({ onSelectListing }) {
  const [stats, setStats] = useState(null);
  const [aiMonitoring, setAIMonitoring] = useState(null);
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    setLoading(true);
    try {
      const [statsData, aiData, listingsData] = await Promise.all([
        api.getAdminStats(),
        api.getAIMonitoring(),
        api.getAdminListings()
      ]);
      setStats(statsData);
      setAIMonitoring(aiData);
      setListings(listingsData);
    } catch (err) {
      console.error('Error fetching admin telemetry:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFlag = async (listingId, newStatus) => {
    try {
      await api.flagListing(listingId, newStatus);
      setListings(prev => prev.map(l => l.id === listingId ? { ...l, status: newStatus } : l));
    } catch (err) {
      alert('Error updating status: ' + err.message);
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-20 text-center">
        <RefreshCw className="w-8 h-8 text-purple-600 animate-spin mx-auto mb-3" />
        <p className="text-gray-500 text-sm">Loading admin telemetry & AI governance...</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Shield className="w-6 h-6 text-purple-600" />
          Admin Governance & AI Telemetry
        </h1>
        <p className="text-gray-500 text-sm">Monitor platform metrics, MobileNetV2 confidence distribution, and inventory moderation.</p>
      </div>

      {/* KPI Cards */}
      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl bg-white border border-gray-200 shadow-sm">
            <span className="text-xs font-bold text-gray-500 uppercase">Registered Users</span>
            <p className="text-2xl font-black text-gray-900 mt-1">{stats.total_users}</p>
          </div>
          <div className="p-5 rounded-2xl bg-white border border-gray-200 shadow-sm">
            <span className="text-xs font-bold text-gray-500 uppercase">Total Listings</span>
            <p className="text-2xl font-black text-purple-600 mt-1">{stats.total_listings}</p>
          </div>
          <div className="p-5 rounded-2xl bg-white border border-gray-200 shadow-sm">
            <span className="text-xs font-bold text-gray-500 uppercase">Completed Trades</span>
            <p className="text-2xl font-black text-emerald-600 mt-1">{stats.total_transactions}</p>
          </div>
          <div className="p-5 rounded-2xl bg-white border border-gray-200 shadow-sm">
            <span className="text-xs font-bold text-gray-500 uppercase">Diverted Waste</span>
            <p className="text-2xl font-black text-teal-600 mt-1">{stats.total_diverted_tonnes} tonnes</p>
          </div>
        </div>
      )}

      {/* AI Telemetry & Quality Control */}
      {aiMonitoring && (
        <div className="p-6 rounded-2xl bg-purple-50/50 border border-purple-200">
          <h2 className="text-base font-bold text-purple-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-purple-600" />
            Computer Vision & Valuation Model Telemetry
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            <div className="p-3 bg-white rounded-xl border border-purple-100">
              <span className="text-gray-500">Average Vision Confidence</span>
              <p className="text-xl font-bold text-purple-900 mt-0.5">{(aiMonitoring.average_confidence * 100).toFixed(1)}%</p>
            </div>
            <div className="p-3 bg-white rounded-xl border border-purple-100">
              <span className="text-gray-500">Classification Accuracy</span>
              <p className="text-xl font-bold text-emerald-700 mt-0.5">{(aiMonitoring.classification_accuracy * 100).toFixed(1)}%</p>
            </div>
            <div className="p-3 bg-white rounded-xl border border-purple-100">
              <span className="text-gray-500">Price Regressor R²</span>
              <p className="text-xl font-bold text-blue-700 mt-0.5">{aiMonitoring.model_r2_score}</p>
            </div>
            <div className="p-3 bg-white rounded-xl border border-purple-100">
              <span className="text-gray-500">User Correction Rate</span>
              <p className="text-xl font-bold text-gray-900 mt-0.5">{aiMonitoring.user_correction_rate}%</p>
            </div>
          </div>
        </div>
      )}

      {/* Moderation Table */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm overflow-x-auto">
        <h2 className="text-lg font-bold text-gray-900 mb-4">Inventory Moderation Queue</h2>
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-gray-100 text-gray-400 uppercase tracking-wider">
              <th className="pb-3 font-semibold">Material</th>
              <th className="pb-3 font-semibold">Category</th>
              <th className="pb-3 font-semibold">Location</th>
              <th className="pb-3 font-semibold">Status</th>
              <th className="pb-3 font-semibold text-right">Moderation</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {listings.map(item => (
              <tr key={item.id} className="hover:bg-gray-50">
                <td className="py-3 font-bold text-gray-900">{item.material_name}</td>
                <td className="py-3 text-gray-600">{item.category}</td>
                <td className="py-3 text-gray-600">{item.city}, {item.state}</td>
                <td className="py-3">
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold capitalize ${
                    item.status === 'active' ? 'bg-emerald-100 text-emerald-800' :
                    item.status === 'flagged' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-600'
                  }`}>
                    {item.status}
                  </span>
                </td>
                <td className="py-3 text-right space-x-2">
                  {item.status !== 'flagged' ? (
                    <button
                      onClick={() => handleFlag(item.id, 'flagged')}
                      className="px-2.5 py-1 text-red-600 hover:bg-red-50 rounded font-semibold text-[11px] transition"
                    >
                      Flag
                    </button>
                  ) : (
                    <button
                      onClick={() => handleFlag(item.id, 'active')}
                      className="px-2.5 py-1 text-emerald-600 hover:bg-emerald-50 rounded font-semibold text-[11px] transition"
                    >
                      Approve
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
