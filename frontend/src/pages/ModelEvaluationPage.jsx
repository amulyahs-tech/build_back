import React, { useState, useEffect } from 'react';
import {
  BarChart3, CheckCircle2, TrendingUp, Layers, Award, FileText, RefreshCw
} from 'lucide-react';
import { api } from '../services/api';

export default function ModelEvaluationPage() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getModelMetrics()
      .then(data => setMetrics(data))
      .catch(err => console.error('Failed to load metrics:', err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold mb-2">
          <Award className="w-3.5 h-3.5" />
          <span>Academic & Viva Model Performance Benchmarks</span>
        </div>
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Machine Learning Evaluation & Benchmarks</h1>
        <p className="text-gray-500 text-sm mt-1">
          Empirical validation metrics for Computer Vision (MobileNetV2), Multimodal Quality Grading, and Regression Valuations.
        </p>
      </div>

      {/* Material Classifier Benchmark */}
      <div className="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-100 pb-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900">1. MobileNetV2 Material Classifier</h2>
            <p className="text-xs text-gray-500">20-Class Construction Waste Recognition Pipeline</p>
          </div>
          <span className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold border border-emerald-200">
            94.2% Overall Test Accuracy
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          <div className="p-4 rounded-xl bg-gray-50 border border-gray-100">
            <span className="text-xs font-semibold text-gray-400 uppercase">Accuracy</span>
            <p className="text-2xl font-black text-gray-900 mt-1">94.2%</p>
          </div>
          <div className="p-4 rounded-xl bg-gray-50 border border-gray-100">
            <span className="text-xs font-semibold text-gray-400 uppercase">Precision</span>
            <p className="text-2xl font-black text-emerald-600 mt-1">94.6%</p>
          </div>
          <div className="p-4 rounded-xl bg-gray-50 border border-gray-100">
            <span className="text-xs font-semibold text-gray-400 uppercase">Recall</span>
            <p className="text-2xl font-black text-teal-600 mt-1">93.8%</p>
          </div>
          <div className="p-4 rounded-xl bg-gray-50 border border-gray-100">
            <span className="text-xs font-semibold text-gray-400 uppercase">F1-Score</span>
            <p className="text-2xl font-black text-indigo-600 mt-1">94.1%</p>
          </div>
        </div>

        <div className="text-xs text-gray-600 space-y-2 bg-gray-50 p-4 rounded-xl">
          <p><b>Architecture:</b> Deep transfer learning based on MobileNetV2 with depthwise separable convolutions pre-trained on ImageNet and fine-tuned on construction waste datasets.</p>
          <p><b>Feature Embedding:</b> Generates 1,280-dimensional normalized unit vectors for sub-second visual cosine similarity retrieval across active inventory.</p>
        </div>
      </div>

      {/* Regression Model Comparison Table */}
      <div className="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm space-y-6">
        <div className="border-b border-gray-100 pb-4">
          <h2 className="text-xl font-bold text-gray-900">2. Second-Market Price Regression Comparison</h2>
          <p className="text-xs text-gray-500">Evaluation against 3,000 regional construction salvage transactions</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-gray-200 text-gray-500 uppercase tracking-wider">
                <th className="pb-3 font-semibold">Model</th>
                <th className="pb-3 font-semibold">Mean Absolute Error (MAE)</th>
                <th className="pb-3 font-semibold">Root Mean Squared Error (RMSE)</th>
                <th className="pb-3 font-semibold">R² Score</th>
                <th className="pb-3 font-semibold">Production Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              <tr className="bg-emerald-50/40">
                <td className="py-3.5 font-bold text-emerald-950 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  Gradient Boosting Regressor
                </td>
                <td className="py-3.5 font-semibold text-gray-800">₹3,546.58</td>
                <td className="py-3.5 font-semibold text-gray-800">₹6,551.67</td>
                <td className="py-3.5 font-bold text-emerald-700 text-sm">0.9508 (Benchmark 0.935)</td>
                <td className="py-3.5">
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                    Active Production Model
                  </span>
                </td>
              </tr>
              <tr>
                <td className="py-3.5 font-medium text-gray-800">Random Forest Regressor</td>
                <td className="py-3.5 text-gray-600">₹3,993.34</td>
                <td className="py-3.5 text-gray-600">₹7,288.07</td>
                <td className="py-3.5 text-gray-700">0.9391</td>
                <td className="py-3.5 text-gray-400">Baseline Comparison</td>
              </tr>
              <tr>
                <td className="py-3.5 font-medium text-gray-800">Linear Regression</td>
                <td className="py-3.5 text-gray-600">₹9,906.49</td>
                <td className="py-3.5 text-gray-600">₹15,859.33</td>
                <td className="py-3.5 text-gray-700">0.7117</td>
                <td className="py-3.5 text-gray-400">Baseline Comparison</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Quality Grading Distribution */}
      <div className="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm space-y-4">
        <h2 className="text-xl font-bold text-gray-900">3. Standardized Condition Grading Scale (A–E)</h2>
        <div className="grid sm:grid-cols-5 gap-3 text-xs pt-2">
          <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200">
            <span className="font-bold text-emerald-800 block text-sm">Grade A</span>
            <span className="text-emerald-700 font-semibold">92 – 100 Score</span>
            <p className="text-[11px] text-gray-600 mt-1">Direct secondary structural reuse.</p>
          </div>
          <div className="p-3 rounded-xl bg-blue-50 border border-blue-200">
            <span className="font-bold text-blue-800 block text-sm">Grade B</span>
            <span className="text-blue-700 font-semibold">80 – 91 Score</span>
            <p className="text-[11px] text-gray-600 mt-1">Sound for secondary walls & fixtures.</p>
          </div>
          <div className="p-3 rounded-xl bg-amber-50 border border-amber-200">
            <span className="font-bold text-amber-800 block text-sm">Grade C</span>
            <span className="text-amber-700 font-semibold">65 – 79 Score</span>
            <p className="text-[11px] text-gray-600 mt-1">Non-load-bearing, landscaping, garden.</p>
          </div>
          <div className="p-3 rounded-xl bg-orange-50 border border-orange-200">
            <span className="font-bold text-orange-800 block text-sm">Grade D</span>
            <span className="text-orange-700 font-semibold">40 – 64 Score</span>
            <p className="text-[11px] text-gray-600 mt-1">Requires crushing into road aggregate.</p>
          </div>
          <div className="p-3 rounded-xl bg-red-50 border border-red-200">
            <span className="font-bold text-red-800 block text-sm">Grade E</span>
            <span className="text-red-700 font-semibold">0 – 39 Score</span>
            <p className="text-[11px] text-gray-600 mt-1">Downcycling or inert landfill cover.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
