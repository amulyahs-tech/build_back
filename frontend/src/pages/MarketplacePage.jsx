import React, { useState, useEffect } from 'react';
import {
  Search, Filter, SlidersHorizontal, Camera, Sparkles, MapPin,
  CheckCircle2, ArrowRight, Heart, X, RefreshCw
} from 'lucide-react';
import { api } from '../services/api';
import CameraCaptureModal from '../components/CameraCaptureModal';

export default function MarketplacePage({ onSelectListing }) {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedGrade, setSelectedGrade] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [sortBy, setSortBy] = useState('newest');

  // Similar Image Search Modal
  const [similarModalOpen, setSimilarModalOpen] = useState(false);
  const [similarCameraOpen, setSimilarCameraOpen] = useState(false);
  const [similarResults, setSimilarResults] = useState(null);
  const [similarSearching, setSimilarSearching] = useState(false);

  useEffect(() => {
    fetchListings();
  }, [selectedCategory, selectedGrade, selectedCity, sortBy]);

  const fetchListings = async () => {
    setLoading(true);
    try {
      const params = { sort_by: sortBy };
      if (selectedCategory) params.category = selectedCategory;
      if (selectedGrade) params.quality_grade = selectedGrade;
      if (selectedCity) params.city = selectedCity;
      if (searchQuery) params.search = searchQuery;

      const data = await api.getListings(params);
      setListings(data);
    } catch (err) {
      console.error('Failed to fetch listings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchListings();
  };

  const handleSimilarPhoto = async (dataUrl) => {
    setSimilarSearching(true);
    setSimilarModalOpen(true);
    try {
      const results = await api.searchSimilar(dataUrl);
      setSimilarResults(results);
    } catch (err) {
      console.error('Similar search error:', err);
      alert('Unable to find similar materials: ' + err.message);
    } finally {
      setSimilarSearching(false);
    }
  };

  const handleSimilarFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      handleSimilarPhoto(ev.target.result);
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Marketplace Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Construction Materials Marketplace</h1>
          <p className="text-gray-500 text-sm mt-1">Verified circular inventory from contractors, demolition sites, and salvage yards.</p>
        </div>

        {/* Visual Similarity Search Button */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSimilarCameraOpen(true)}
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 rounded-xl text-sm font-semibold transition shadow-sm"
          >
            <Camera className="w-4 h-4 text-emerald-600" />
            <span>Find Visually Similar (Camera)</span>
          </button>
          <label className="inline-flex items-center gap-2 px-4 py-2.5 bg-white hover:bg-gray-50 border border-gray-200 text-gray-700 rounded-xl text-sm font-semibold transition cursor-pointer shadow-sm">
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>Upload Image Search</span>
            <input type="file" accept="image/*" onChange={handleSimilarFileUpload} className="hidden" />
          </label>
        </div>
      </div>

      {/* Filter & Search Toolbar */}
      <div className="p-4 rounded-2xl bg-white border border-gray-200 shadow-sm space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search by material (e.g. Red Brick, TMT Steel, Teak, Aggregate)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold rounded-xl transition"
          >
            Search
          </button>
        </form>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 border-t border-gray-100">
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-3 py-2 border border-gray-200 rounded-lg text-xs font-medium text-gray-700 bg-gray-50/50"
          >
            <option value="">All Categories</option>
            <option value="Masonry">Masonry</option>
            <option value="Metals & Structural">Metals & Structural</option>
            <option value="Aggregates & Masonry">Aggregates & Masonry</option>
            <option value="Lumber & Carpentry">Lumber & Carpentry</option>
            <option value="Finishing & Ceramics">Finishing & Ceramics</option>
            <option value="Plumbing & Conduits">Plumbing & Conduits</option>
            <option value="Finishing & Flooring">Finishing & Flooring</option>
            <option value="Glazing & Openings">Glazing & Openings</option>
          </select>

          <select
            value={selectedGrade}
            onChange={(e) => setSelectedGrade(e.target.value)}
            className="px-3 py-2 border border-gray-200 rounded-lg text-xs font-medium text-gray-700 bg-gray-50/50"
          >
            <option value="">All Quality Grades</option>
            <option value="A">Grade A (92-100 Excellent)</option>
            <option value="B">Grade B (80-91 Good)</option>
            <option value="C">Grade C (65-79 Moderate)</option>
            <option value="D">Grade D (40-64 Poor)</option>
            <option value="E">Grade E (0-39 Very Poor)</option>
          </select>

          <select
            value={selectedCity}
            onChange={(e) => setSelectedCity(e.target.value)}
            className="px-3 py-2 border border-gray-200 rounded-lg text-xs font-medium text-gray-700 bg-gray-50/50"
          >
            <option value="">All Cities</option>
            <option value="Bangalore">Bangalore</option>
            <option value="Mumbai">Mumbai</option>
            <option value="Delhi">Delhi</option>
            <option value="Hyderabad">Hyderabad</option>
            <option value="Pune">Pune</option>
            <option value="Mysore">Mysore</option>
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 border border-gray-200 rounded-lg text-xs font-medium text-gray-700 bg-gray-50/50"
          >
            <option value="newest">Sort: Newest First</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="quality">Quality Condition</option>
          </select>
        </div>
      </div>

      {/* Listings Grid */}
      {loading ? (
        <div className="text-center py-20">
          <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin mx-auto mb-3" />
          <p className="text-gray-500 text-sm">Loading active circular inventory...</p>
        </div>
      ) : listings.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-2xl border border-gray-200 p-8">
          <Search className="w-12 h-12 text-gray-400 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-gray-900 mb-1">No matching materials found</h3>
          <p className="text-gray-500 text-sm max-w-sm mx-auto mb-4">
            Try adjusting your search criteria or clear active filters to discover other construction salvage lots.
          </p>
          <button
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('');
              setSelectedGrade('');
              setSelectedCity('');
            }}
            className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-xs font-semibold"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {listings.map(item => (
            <div
              key={item.id}
              onClick={() => onSelectListing(item.id)}
              className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md hover:border-emerald-300 transition overflow-hidden cursor-pointer group flex flex-col justify-between"
            >
              <div>
                <div className="relative h-48 overflow-hidden bg-gray-100">
                  <img
                    src={item.image_url}
                    alt={item.material_name}
                    className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                  />
                  <div className="absolute top-3 left-3">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold shadow-sm ${
                      item.quality_grade === 'A' ? 'bg-emerald-500 text-white' :
                      item.quality_grade === 'B' ? 'bg-blue-600 text-white' :
                      item.quality_grade === 'C' ? 'bg-amber-500 text-white' : 'bg-red-500 text-white'
                    }`}>
                      Grade {item.quality_grade} ({item.quality_score.toFixed(0)}/100)
                    </span>
                  </div>
                  <div className="absolute top-3 right-3">
                    <span className="px-2.5 py-1 rounded-full text-[10px] font-semibold bg-black/60 text-white backdrop-blur-sm">
                      {item.category}
                    </span>
                  </div>
                </div>

                <div className="p-5">
                  <h3 className="font-bold text-gray-900 text-base mb-1 group-hover:text-emerald-600 transition">
                    {item.material_name}
                  </h3>
                  <p className="text-xs text-gray-500 flex items-center gap-1 mb-3">
                    <MapPin className="w-3.5 h-3.5 text-gray-400" />
                    {item.city}, {item.state}
                  </p>
                  <p className="text-xs text-gray-600 line-clamp-2 mb-4">
                    Salvaged from: <span className="font-medium text-gray-800">{item.original_usage}</span>
                  </p>
                </div>
              </div>

              <div className="px-5 pb-5 pt-3 border-t border-gray-100 flex items-center justify-between">
                <div>
                  <span className="text-xl font-extrabold text-emerald-700">₹{item.price.toLocaleString()}</span>
                  <p className="text-[11px] text-gray-500 font-medium">{item.quantity.toLocaleString()} {item.unit}</p>
                </div>
                <button
                  type="button"
                  className="px-3.5 py-1.5 bg-emerald-50 text-emerald-700 hover:bg-emerald-600 hover:text-white rounded-lg text-xs font-semibold transition flex items-center gap-1"
                >
                  View Details <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Visual Similarity Search Modal */}
      {similarModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <div className="flex items-center gap-2 text-emerald-800 font-bold text-lg">
                <Sparkles className="w-5 h-5 text-emerald-600" />
                <span>Visual Similarity Search Results</span>
              </div>
              <button
                onClick={() => {
                  setSimilarModalOpen(false);
                  setSimilarResults(null);
                }}
                className="p-1 text-gray-400 hover:text-gray-600 rounded-full"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {similarSearching ? (
              <div className="text-center py-12">
                <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin mx-auto mb-3" />
                <p className="text-sm font-semibold text-gray-800">Matching 1280-dim feature embeddings against inventory...</p>
              </div>
            ) : similarResults && similarResults.length > 0 ? (
              <div className="space-y-3 max-h-[60vh] overflow-y-auto pr-1">
                {similarResults.map(res => (
                  <div
                    key={res.id}
                    onClick={() => {
                      setSimilarModalOpen(false);
                      onSelectListing(res.id);
                    }}
                    className="flex items-center justify-between p-3 rounded-xl border border-gray-200 hover:border-emerald-500 hover:bg-emerald-50/30 transition cursor-pointer"
                  >
                    <div className="flex items-center gap-3">
                      <img src={res.image_url} alt={res.material_name} className="w-14 h-14 rounded-lg object-cover" />
                      <div>
                        <h4 className="text-sm font-bold text-gray-900">{res.material_name}</h4>
                        <p className="text-xs text-gray-500">📍 {res.city} • Grade {res.quality_grade}</p>
                        <span className="text-xs font-semibold text-emerald-700">₹{res.price.toLocaleString()}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold">
                        {res.similarity_score}% Match
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500 text-sm">
                No visually similar materials found above the confidence threshold.
              </div>
            )}
          </div>
        </div>
      )}

      {/* Camera Capture Modal for Similarity Search */}
      <CameraCaptureModal
        isOpen={similarCameraOpen}
        onClose={() => setSimilarCameraOpen(false)}
        onPhotoCaptured={handleSimilarPhoto}
      />
    </div>
  );
}
