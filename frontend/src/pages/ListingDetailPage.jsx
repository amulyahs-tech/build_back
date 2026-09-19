import React, { useState, useEffect } from 'react';
import {
  MapPin, CheckCircle2, AlertTriangle, ArrowLeft, Heart, Send,
  ShieldCheck, Leaf, Sparkles, Building, Calendar, Phone, Check, RefreshCw
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function ListingDetailPage({ listingId, onBack, onNavigate }) {
  const { user } = useAuth();
  const [listing, setListing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);

  // Purchase Request Dialog State
  const [dialogOpen, setDialogOpen] = useState(false);
  const [proposedPrice, setProposedPrice] = useState('');
  const [requestQty, setRequestQty] = useState('');
  const [message, setMessage] = useState('');
  const [pickupDate, setPickupDate] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [requestSuccess, setRequestSuccess] = useState(false);

  useEffect(() => {
    fetchListing();
  }, [listingId]);

  const fetchListing = async () => {
    setLoading(true);
    try {
      const data = await api.getListingDetail(listingId);
      setListing(data);
      setProposedPrice(data.price);
      setRequestQty(data.quantity);
    } catch (err) {
      console.error('Failed to load listing details:', err);
      setErrorMsg(err.message || 'Unable to load listing details.');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleFav = async () => {
    if (!user) {
      alert('Please sign in to save favorite materials.');
      onNavigate('login');
      return;
    }
    try {
      const res = await api.toggleFavorite(listing.id);
      setListing(prev => ({ ...prev, is_favorited: res.favorited }));
    } catch (err) {
      console.error('Favorite toggle failed:', err);
    }
  };

  const handleSubmitPurchaseRequest = async (e) => {
    e.preventDefault();
    if (!user) {
      alert('Please sign in to submit a purchase request.');
      onNavigate('login');
      return;
    }
    setSubmitting(true);
    try {
      await api.createPurchaseRequest({
        listing_id: listing.id,
        quantity: parseFloat(requestQty),
        proposed_price: parseFloat(proposedPrice),
        message: message,
        preferred_pickup_date: pickupDate || 'As soon as possible'
      });
      setRequestSuccess(true);
    } catch (err) {
      alert('Failed to send offer: ' + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-20 text-center">
        <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin mx-auto mb-3" />
        <p className="text-gray-500 text-sm">Loading listing details...</p>
      </div>
    );
  }

  if (errorMsg || !listing) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center">
        <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-3" />
        <h2 className="text-xl font-bold text-gray-900 mb-2">Listing Not Found</h2>
        <p className="text-gray-600 text-sm mb-6">{errorMsg || 'This material may have already been sold or archived.'}</p>
        <button
          onClick={onBack}
          className="px-5 py-2.5 bg-emerald-600 text-white rounded-xl text-sm font-semibold"
        >
          Return to Marketplace
        </button>
      </div>
    );
  }

  // Estimated LCA factors
  const divertedTonnes = ((listing.quantity * 3.0) / 1000.0).toFixed(2);
  const avoidedCo2 = (listing.quantity * 0.72).toFixed(0);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Back Button */}
      <button
        onClick={onBack}
        className="inline-flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-emerald-700 transition"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Marketplace
      </button>

      <div className="grid lg:grid-cols-2 gap-10">
        {/* Left Column: Image & Visual Verification */}
        <div className="space-y-4">
          <div className="relative rounded-3xl overflow-hidden bg-gray-100 border border-gray-200 shadow-sm max-h-[460px]">
            <img
              src={listing.image_url}
              alt={listing.material_name}
              className="w-full h-full object-cover"
            />
            <div className="absolute top-4 left-4">
              <span className={`px-3 py-1 rounded-full text-xs font-bold shadow-md ${
                listing.quality_grade === 'A' ? 'bg-emerald-500 text-white' :
                listing.quality_grade === 'B' ? 'bg-blue-600 text-white' :
                listing.quality_grade === 'C' ? 'bg-amber-500 text-white' : 'bg-red-500 text-white'
              }`}>
                Quality Grade {listing.quality_grade} ({listing.quality_score.toFixed(0)}/100)
              </span>
            </div>
          </div>

          {/* AI Vision Metadata Card */}
          <div className="p-4 rounded-2xl bg-emerald-50/50 border border-emerald-200 flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 text-emerald-900 font-semibold">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span>MobileNetV2 Vision Confidence: <b>{(listing.ai_confidence * 100).toFixed(1)}%</b></span>
            </div>
            <span className="text-emerald-700 font-medium">{listing.category}</span>
          </div>
        </div>

        {/* Right Column: Listing Details & Offer Action */}
        <div className="space-y-6">
          <div>
            <div className="flex justify-between items-start">
              <h1 className="text-3xl font-extrabold text-gray-900 leading-tight mb-2">
                {listing.material_name}
              </h1>
              <button
                onClick={handleToggleFav}
                className={`p-2.5 rounded-full border transition ${
                  listing.is_favorited ? 'bg-red-50 border-red-200 text-red-600' : 'bg-white border-gray-200 text-gray-400 hover:text-red-500'
                }`}
              >
                <Heart className={`w-5 h-5 ${listing.is_favorited ? 'fill-red-600' : ''}`} />
              </button>
            </div>
            <p className="text-sm text-gray-500 flex items-center gap-1">
              <MapPin className="w-4 h-4 text-gray-400" />
              {listing.city}, {listing.state} • Pickup: <span className="font-medium text-gray-800">{listing.availability}</span>
            </p>
          </div>

          {/* Price & Quantity Box */}
          <div className="p-6 rounded-2xl bg-gray-50 border border-gray-200 flex items-center justify-between">
            <div>
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Asking Price</span>
              <div className="text-3xl font-extrabold text-emerald-700 mt-1">
                ₹{listing.price.toLocaleString()}
              </div>
              <p className="text-xs text-gray-500 mt-0.5">
                Rate: ₹{(listing.price / Math.max(1, listing.quantity)).toFixed(2)} per {listing.unit}
              </p>
            </div>
            <div className="text-right">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Available Quantity</span>
              <div className="text-xl font-bold text-gray-900 mt-1">
                {listing.quantity.toLocaleString()} {listing.unit}
              </div>
              <p className="text-xs text-emerald-600 font-semibold mt-0.5">
                Age: ~{listing.age_years} yrs • Wear: {listing.damage_percentage}%
              </p>
            </div>
          </div>

          {/* Environmental Impact Counter */}
          <div className="p-5 rounded-2xl bg-gradient-to-tr from-emerald-900 to-teal-900 text-white shadow-lg space-y-2">
            <span className="text-xs font-bold text-emerald-300 uppercase tracking-wider flex items-center gap-1.5">
              <Leaf className="w-4 h-4" /> Certified Circular Impact
            </span>
            <div className="grid grid-cols-2 gap-4 pt-1">
              <div>
                <p className="text-2xl font-black text-white">{divertedTonnes} tonnes</p>
                <p className="text-[11px] text-emerald-200">Estimated Landfill Diversion</p>
              </div>
              <div>
                <p className="text-2xl font-black text-teal-300">{avoidedCo2} kg CO₂e</p>
                <p className="text-[11px] text-emerald-200">Avoided Embodied Carbon</p>
              </div>
            </div>
          </div>

          {/* Seller & Action Buttons */}
          <div className="p-4 rounded-xl border border-gray-200 bg-white flex items-center justify-between">
            <div className="text-xs">
              <span className="text-gray-400 block">Listed by Seller:</span>
              <span className="font-bold text-gray-900 text-sm">{listing.seller_name}</span>
              {listing.seller_phone && (
                <span className="text-gray-500 flex items-center gap-1 mt-0.5">
                  <Phone className="w-3 h-3 text-emerald-600" /> {listing.seller_phone}
                </span>
              )}
            </div>
            <button
              onClick={() => setDialogOpen(true)}
              className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm rounded-xl shadow-md shadow-emerald-600/20 transition flex items-center gap-2"
            >
              <Send className="w-4 h-4" />
              Make Purchase Offer
            </button>
          </div>

          <p className="text-[11px] text-gray-400 italic">
            * AI visual assessment is an advisory condition estimate. Professional civil inspection is recommended for critical load-bearing installations.
          </p>
        </div>
      </div>

      {/* Purchase Request Modal */}
      {dialogOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl">
            {requestSuccess ? (
              <div className="text-center py-6">
                <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto mb-3">
                  <Check className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-1">Offer Submitted!</h3>
                <p className="text-xs text-gray-600 mb-6">
                  The seller will review your offer and notify you upon acceptance.
                </p>
                <button
                  onClick={() => {
                    setDialogOpen(false);
                    setRequestSuccess(false);
                  }}
                  className="w-full py-2.5 bg-emerald-600 text-white font-semibold rounded-xl text-sm"
                >
                  Done
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmitPurchaseRequest} className="space-y-4">
                <h3 className="text-lg font-bold text-gray-900">Make an Offer on {listing.material_name}</h3>
                <p className="text-xs text-gray-500">Listed Asking Price: ₹{listing.price.toLocaleString()} ({listing.quantity} {listing.unit})</p>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Proposed Total Price (₹)</label>
                  <input
                    type="number"
                    required
                    value={proposedPrice}
                    onChange={(e) => setProposedPrice(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm font-bold text-emerald-900"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Quantity Requested ({listing.unit})</label>
                  <input
                    type="number"
                    required
                    max={listing.quantity}
                    value={requestQty}
                    onChange={(e) => setRequestQty(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Preferred Pickup Date</label>
                  <input
                    type="date"
                    value={pickupDate}
                    onChange={(e) => setPickupDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Message to Seller (Optional)</label>
                  <textarea
                    rows="2"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="We have transport ready for Friday morning..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs"
                  />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setDialogOpen(false)}
                    className="px-4 py-2 border border-gray-300 rounded-lg text-xs font-medium text-gray-700"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition"
                  >
                    {submitting ? 'Submitting...' : 'Submit Purchase Offer'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
