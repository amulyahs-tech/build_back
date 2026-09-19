import React, { useState, useEffect } from 'react';
import {
  Package, DollarSign, Check, X, Clock, AlertCircle, RefreshCw, Trash2, ExternalLink
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function SellerDashboard({ onNavigate }) {
  const { user } = useAuth();
  const [myListings, setMyListings] = useState([]);
  const [incomingRequests, setIncomingRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [listings, requests] = await Promise.all([
        api.getMyListings(),
        api.getIncomingRequests()
      ]);
      setMyListings(listings);
      setIncomingRequests(requests);
    } catch (err) {
      console.error('Error loading seller dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRequestAction = async (requestId, status) => {
    setActionLoading(true);
    try {
      await api.updatePurchaseRequest(requestId, status);
      await loadData();
    } catch (err) {
      alert('Error updating request: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleDeleteListing = async (listingId) => {
    if (!confirm('Are you sure you want to delete this listing?')) return;
    try {
      await api.deleteListing(listingId);
      setMyListings(prev => prev.filter(l => l.id !== listingId));
    } catch (err) {
      alert('Failed to delete listing: ' + err.message);
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-20 text-center">
        <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin mx-auto mb-3" />
        <p className="text-gray-500 text-sm">Loading seller dashboard...</p>
      </div>
    );
  }

  const activeCount = myListings.filter(l => l.status === 'active').length;
  const soldCount = myListings.filter(l => l.status === 'sold').length;
  const totalValue = myListings.reduce((sum, l) => sum + (l.price || 0), 0);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Seller Hub & Inventory</h1>
        <p className="text-gray-500 text-sm">Manage listed surplus materials and respond to contractor purchase offers.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 rounded-2xl bg-white border border-gray-200 shadow-sm">
          <span className="text-xs font-bold text-gray-500 uppercase">Active Materials</span>
          <p className="text-2xl font-black text-gray-900 mt-1">{activeCount}</p>
        </div>
        <div className="p-5 rounded-2xl bg-white border border-gray-200 shadow-sm">
          <span className="text-xs font-bold text-gray-500 uppercase">Sold / Completed</span>
          <p className="text-2xl font-black text-emerald-600 mt-1">{soldCount}</p>
        </div>
        <div className="p-5 rounded-2xl bg-white border border-gray-200 shadow-sm">
          <span className="text-xs font-bold text-gray-500 uppercase">Total Inventory Value</span>
          <p className="text-2xl font-black text-emerald-700 mt-1">₹{totalValue.toLocaleString()}</p>
        </div>
      </div>

      {/* Incoming Buyer Offers */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
        <h2 className="text-lg font-bold text-gray-900 mb-4">Incoming Buyer Offers ({incomingRequests.length})</h2>

        {incomingRequests.length === 0 ? (
          <p className="text-gray-500 text-sm py-4">No offers received yet. Your active listings will show offers here.</p>
        ) : (
          <div className="space-y-3">
            {incomingRequests.map(req => (
              <div key={req.id} className="p-4 rounded-xl border border-gray-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <span className="text-xs font-bold text-emerald-700 uppercase">{req.material_name}</span>
                  <div className="text-sm font-semibold text-gray-900 mt-0.5">
                    Offered ₹{req.proposed_price.toLocaleString()} for {req.quantity} units
                  </div>
                  <p className="text-xs text-gray-500">
                    From: <span className="font-medium text-gray-700">{req.buyer_name}</span> • Pickup: {req.preferred_pickup_date || 'Flexible'}
                  </p>
                  {req.message && <p className="text-xs text-gray-600 italic mt-1">"{req.message}"</p>}
                </div>

                <div className="flex items-center gap-2">
                  {req.status === 'pending' ? (
                    <>
                      <button
                        onClick={() => handleRequestAction(req.id, 'accepted')}
                        disabled={actionLoading}
                        className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition flex items-center gap-1"
                      >
                        <Check className="w-4 h-4" /> Accept Offer
                      </button>
                      <button
                        onClick={() => handleRequestAction(req.id, 'rejected')}
                        disabled={actionLoading}
                        className="px-4 py-2 border border-gray-300 text-gray-700 hover:bg-gray-50 rounded-lg text-xs font-medium transition flex items-center gap-1"
                      >
                        <X className="w-4 h-4" /> Decline
                      </button>
                    </>
                  ) : (
                    <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
                      req.status === 'accepted' ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {req.status}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Inventory Listings Table */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm overflow-x-auto">
        <h2 className="text-lg font-bold text-gray-900 mb-4">Your Listed Materials ({myListings.length})</h2>

        {myListings.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500 text-sm mb-4">You haven't listed any surplus construction materials yet.</p>
            <button
              onClick={() => onNavigate('wizard')}
              className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-xs font-bold"
            >
              List Your First Material
            </button>
          </div>
        ) : (
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-gray-100 text-gray-400 uppercase tracking-wider">
                <th className="pb-3 font-semibold">Material</th>
                <th className="pb-3 font-semibold">Grade</th>
                <th className="pb-3 font-semibold">Quantity</th>
                <th className="pb-3 font-semibold">Price</th>
                <th className="pb-3 font-semibold">Status</th>
                <th className="pb-3 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {myListings.map(item => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="py-3 font-bold text-gray-900">{item.material_name}</td>
                  <td className="py-3">
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                      Grade {item.quality_grade}
                    </span>
                  </td>
                  <td className="py-3 text-gray-600">{item.quantity} {item.unit}</td>
                  <td className="py-3 font-bold text-emerald-700">₹{item.price.toLocaleString()}</td>
                  <td className="py-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold capitalize ${
                      item.status === 'active' ? 'bg-emerald-50 text-emerald-700' : 'bg-gray-100 text-gray-600'
                    }`}>
                      {item.status}
                    </span>
                  </td>
                  <td className="py-3 text-right">
                    <button
                      onClick={() => handleDeleteListing(item.id)}
                      className="p-1 text-gray-400 hover:text-red-600 transition"
                      title="Delete listing"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
