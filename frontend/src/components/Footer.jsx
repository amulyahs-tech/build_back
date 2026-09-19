import React from 'react';
import { Recycle, Heart, Globe, Shield } from 'lucide-react';

export default function Footer({ onNavigate }) {
  return (
    <footer className="bg-slate-900 text-slate-300 pt-12 pb-8 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-white font-bold text-lg">
              <Recycle className="w-5 h-5 text-emerald-400" />
              <span>REBUILD AI</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              AI-Powered Construction Waste Reuse & Second-Market Platform enabling demolition contractors, builders, and recyclers to circularize building materials.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white mb-3">Marketplace</h4>
            <ul className="text-xs space-y-2 text-slate-400">
              <li><button onClick={() => onNavigate('marketplace')} className="hover:text-emerald-400">Browse Listings</button></li>
              <li><button onClick={() => onNavigate('wizard')} className="hover:text-emerald-400">Sell Surplus Materials</button></li>
              <li><button onClick={() => onNavigate('marketplace')} className="hover:text-emerald-400">Visual Similarity Search</button></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white mb-3">Technology & AI</h4>
            <ul className="text-xs space-y-2 text-slate-400">
              <li><button onClick={() => onNavigate('evaluation')} className="hover:text-emerald-400">MobileNetV2 Classifier</button></li>
              <li><button onClick={() => onNavigate('evaluation')} className="hover:text-emerald-400">Gradient Boosting Regressor</button></li>
              <li><button onClick={() => onNavigate('evaluation')} className="hover:text-emerald-400">Circular LCA Model</button></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white mb-3">Compliance & Safety</h4>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              AI condition grading provides non-binding visual guidance. Load-bearing structures require on-site physical material inspection by registered civil engineers.
            </p>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-800 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-500 gap-4">
          <p>© 2026 REBUILD AI Platform. All rights reserved.</p>
          <div className="flex items-center gap-4">
            <span>Built for Sustainable Infrastructure</span>
            <span>•</span>
            <span>MIT License</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
