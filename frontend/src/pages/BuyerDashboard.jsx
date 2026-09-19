import React, { useState, useEffect } from 'react';
import { ShoppingBag, Heart, Clock, CheckCircle2, XCircle, RefreshCw, ArrowRight } from 'lucide-react';
import { api } from '../services/api';

export default function BuyerDashboard({ onSelectListing, onNavigate }) {
  const [favorites, setFavorites] = useState([]);
  const [purchaseRequests, setPurchaseRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [favs, reqs] = await Promise.all([
        api.getMyFavorites(),
        api.getMyPurchaseRequests()
      ]);
      setFavorites(favs);
      setPurchaseRequests(reqs);
    } catch (err) {
      console.error('Error loading buyer data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-20 text-center">
        <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin mx-auto mb-3" />
        <p className="text-gray-500 text-sm">Loading buyer orders & saved materials...</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Buyer Portal & Orders</h1>
        <p className="text-gray-500 text-sm">Track your purchase offers and saved secondary construction materials.</p>
      </div>

      {/* Sent Offers Table */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
        <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Clock className="w-5 h-5 text-emerald-600" />
          Your Purchase Offers ({purchaseRequests.length})
        </h2>

        {purchaseRequests.length === 0 ? (
          <div className="text-center py-8 text-gray-500 text-sm">
            You haven't submitted any purchase requests yet.
            <div className="mt-3">
              <button
                onClick={() => onNavigate('marketplace')}
                className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-xs font-semibold"
              >
                Browse Marketplace
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            {purchaseRequests.map(req => (
              <div key={req.id} className="p-4 rounded-xl border border-gray-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h4 className="font-bold text-gray-900 text-sm">{req.material_name}</h4>
                  <p className="text-xs text-gray-500 mt-0.5">
                    Offered <b>₹{req.proposed_price.toLocaleString()}</b> for <b>{req.quantity} units</b>
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">Seller: {req.seller_name || 'Demolition Supplier'}</p>
                </div>

                <div>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase flex items-center gap-1.5 ${
                    req.status === 'accepted' ? 'bg-emerald-100 text-emerald-800' :
                    req.status === 'rejected' ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {req.status === 'accepted' && <CheckCircle2 className="w-3.5 h-3.5" />}
                    {req.status === 'rejected' && <XCircle className="w-3.5 h-3.5" />}
                    {req.status === 'pending' && <Clock className="w-3.5 h-3.5" />}
                    {req.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Saved / Favorites */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
        <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Heart className="w-5 h-5 text-red-500" />
          Saved Materials ({favorites.length})
        </h2>

        {favorites.length === 0 ? (
          <p className="text-gray-500 text-sm py-4">No materials saved to favorites.</p>
        ) : (
          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
            {favorites.map(item => (
              <div
                key={item.id}
                onClick={() => onSelectListing(item.id)}
                className="p-3 rounded-xl border border-gray-200 hover:border-emerald-500 transition cursor-pointer flex items-center gap-3"
              >
                <img src={item.image_url} alt={item.material_name} className="w-16 h-16 rounded-lg object-cover" />
                <div>
                  <h4 className="text-sm font-bold text-gray-900">{item.material_name}</h4>
                  <p className="text-xs text-emerald-700 font-semibold">₹{item.price.toLocaleString()}</p>
                  <span className="text-[10px] text-gray-400">📍 {item.city}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
