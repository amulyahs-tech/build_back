import React, { useState, useEffect } from 'react';
import {
  Recycle, Camera, ArrowRight, ShieldCheck, TrendingDown, Leaf,
  BarChart, CheckCircle2, ChevronRight, Building2, HardHat, Sparkles
} from 'lucide-react';
import { api } from '../services/api';

export default function LandingPage({ onNavigate }) {
  const [summary, setSummary] = useState({
    total_landfill_diverted_tonnes: 48.5,
    total_co2_saved_kg: 14200.0,
    total_trees_equivalent: 645,
    total_transactions: 18
  });
  const [featuredListings, setFeaturedListings] = useState([]);

  useEffect(() => {
    api.getEnvironmentalSummary()
      .then(data => setSummary(data))
      .catch(err => console.warn('Could not load dynamic environmental summary:', err));

    api.getListings({ sort_by: 'newest' })
      .then(items => setFeaturedListings(items.slice(0, 3)))
      .catch(err => console.warn('Could not load featured listings:', err));
  }, []);

  return (
    <div className="space-y-16 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-50/70 via-white to-white py-20 px-4 sm:px-6 lg:px-8 border-b border-gray-100">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold mb-6 shadow-sm">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI-Powered Construction Waste Reuse & Second-Market Platform</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-900 tracking-tight leading-tight mb-6">
            Give Construction Waste <br className="hidden sm:inline" />
            <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              A Profitable Second Life
            </span>
          </h1>

          <p className="text-base sm:text-lg text-gray-600 max-w-2xl mx-auto mb-10 leading-relaxed">
            Revolutionize circular infrastructure. Identify salvaged building materials from live camera photos,
            grade structural condition A–E, and trade verified surplus with machine-learning pricing.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => onNavigate('wizard')}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-base shadow-lg shadow-emerald-600/25 transition"
            >
              <Camera className="w-5 h-5" />
              Scan & Sell Material
            </button>
            <button
              onClick={() => onNavigate('marketplace')}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-white hover:bg-gray-50 border border-gray-300 text-gray-800 font-semibold text-base shadow-sm transition"
            >
              Explore Marketplace
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Dynamic Circular Counters */}
        <div className="max-w-5xl mx-auto mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 px-4">
          <div className="p-6 rounded-2xl bg-white border border-gray-100 shadow-sm text-center">
            <div className="text-3xl font-extrabold text-emerald-600 mb-1">
              {summary.total_landfill_diverted_tonnes.toLocaleString()}t
            </div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Landfill Diverted</p>
          </div>
          <div className="p-6 rounded-2xl bg-white border border-gray-100 shadow-sm text-center">
            <div className="text-3xl font-extrabold text-teal-600 mb-1">
              {summary.total_co2_saved_kg.toLocaleString()} kg
            </div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Avoided CO₂e</p>
          </div>
          <div className="p-6 rounded-2xl bg-white border border-gray-100 shadow-sm text-center">
            <div className="text-3xl font-extrabold text-blue-600 mb-1">
              {summary.total_trees_equivalent.toLocaleString()}
            </div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Trees Equivalent</p>
          </div>
          <div className="p-6 rounded-2xl bg-white border border-gray-100 shadow-sm text-center">
            <div className="text-3xl font-extrabold text-indigo-600 mb-1">
              {summary.total_transactions}
            </div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Completed Trades</p>
          </div>
        </div>
      </section>

      {/* Problem & Solution */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-4">
            <span className="text-xs font-bold text-red-600 uppercase tracking-wider">The Construction Waste Crisis</span>
            <h2 className="text-3xl font-bold text-gray-900 leading-tight">
              Over 100M+ tonnes of reusable construction material end up in landfills annually.
            </h2>
            <p className="text-sm text-gray-600 leading-relaxed">
              Demolition teams lack standardized grading and pricing benchmarks, while builders lack confidence in buying salvaged materials. REBUILD AI provides transparent computer vision identification, multimodal wear scoring, and verified circular transactions.
            </p>
          </div>

          <div className="space-y-4 p-8 rounded-3xl bg-emerald-900 text-white shadow-xl">
            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">The REBUILD AI Solution</span>
            <h3 className="text-2xl font-bold">End-to-End Circular Economy Intelligence</h3>
            <ul className="space-y-3 text-sm text-emerald-100">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span><b>Instant Mobile Recognition:</b> MobileNetV2 identifies 20 construction waste classes from camera snapshots.</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span><b>Standardized Quality (A–E):</b> Clear wear scores distinguish secondary structural elements from crushed aggregate.</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span><b>Gradient Boosting Pricing:</b> Accurate fair market valuations achieving benchmark $R^2 = 0.935$.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Interactive 6-Step Workflow */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider">System Architecture</span>
          <h2 className="text-3xl font-bold text-gray-900 mt-1">How REBUILD AI Works</h2>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { step: '01', title: 'Camera Capture', desc: 'Point your phone or laptop camera directly at salvaged material on-site.' },
            { step: '02', title: 'Deep Classification', desc: 'MobileNetV2 classifies material and extracts 1280-dim feature vector.' },
            { step: '03', title: 'Quality Grading A–E', desc: 'Assesses degradation, chipping, and cracks for safe secondary usage.' },
            { step: '04', title: 'AI Price Valuation', desc: 'Predicts regional secondary market value and suggested negotiation range.' },
            { step: '05', title: 'Marketplace Match', desc: 'Buyers discover surplus nearby or match visually similar materials.' },
            { step: '06', title: 'Verified Circular LCA', desc: 'Transactions auto-calculate verified landfill diversion and carbon savings.' }
          ].map((item, i) => (
            <div key={i} className="p-6 rounded-2xl bg-white border border-gray-200 shadow-sm hover:border-emerald-500 transition">
              <span className="text-2xl font-black text-emerald-600 mb-2 block">{item.step}</span>
              <h3 className="font-bold text-gray-900 mb-1">{item.title}</h3>
              <p className="text-xs text-gray-500 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Listings Carousel / Grid */}
      {featuredListings.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-end mb-8">
            <div>
              <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider">Live Inventory</span>
              <h2 className="text-2xl font-bold text-gray-900 mt-1">Recently Listed Materials</h2>
            </div>
            <button
              onClick={() => onNavigate('marketplace')}
              className="text-sm font-semibold text-emerald-600 hover:text-emerald-700 flex items-center gap-1"
            >
              View all <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {featuredListings.map(item => (
              <div
                key={item.id}
                onClick={() => onNavigate('marketplace')}
                className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition overflow-hidden cursor-pointer group"
              >
                <img src={item.image_url} alt={item.material_name} className="w-full h-48 object-cover group-hover:scale-105 transition duration-300" />
                <div className="p-5">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-bold text-gray-900 text-base">{item.material_name}</h4>
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
                      Grade {item.quality_grade}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mb-3">📍 {item.city}, {item.state}</p>
                  <div className="flex justify-between items-center pt-3 border-t border-gray-100">
                    <span className="text-lg font-bold text-emerald-700">₹{item.price.toLocaleString()}</span>
                    <span className="text-xs text-gray-500 font-medium">{item.quantity} {item.unit}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Bottom CTA Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="rounded-3xl bg-gradient-to-r from-emerald-600 to-teal-700 p-8 sm:p-12 text-center text-white shadow-xl">
          <h2 className="text-3xl font-extrabold mb-3">Ready to Circularize Your Construction Waste?</h2>
          <p className="text-emerald-100 text-sm max-w-xl mx-auto mb-8">
            Join hundreds of sustainable contractors and recyclers reducing embodied carbon and maximizing salvage revenue.
          </p>
          <button
            onClick={() => onNavigate('wizard')}
            className="px-8 py-3.5 rounded-xl bg-white text-emerald-800 font-bold text-base hover:bg-emerald-50 shadow-lg transition"
          >
            Start Material AI Scan Now
          </button>
        </div>
      </section>
    </div>
  );
}
