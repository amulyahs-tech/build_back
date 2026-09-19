import React, { useState } from 'react';
import {
  Camera, Upload, Sparkles, CheckCircle2, AlertTriangle, ArrowRight, ArrowLeft,
  DollarSign, Leaf, RefreshCw, Layers, ShieldCheck, MapPin, Check
} from 'lucide-react';
import CameraCaptureModal from '../components/CameraCaptureModal';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

const MATERIAL_OPTIONS = [
  "Bricks", "Concrete", "Cement Blocks", "Steel / Rebar", "Wood / Timber",
  "Tiles", "Glass", "PVC Pipes", "Metal Pipes", "Doors", "Windows",
  "Electrical Components", "Roofing Materials", "Stones", "Sand", "Marble",
  "Granite", "Ceramic Materials", "Mixed Construction Waste", "Other / Debris"
];

export default function CreateListingWizard({ onNavigate, initialData = null }) {
  const { user } = useAuth();
  const [step, setStep] = useState(initialData?.valuationData ? 3 : 1);
  const [cameraModalOpen, setCameraModalOpen] = useState(false);

  // Form State
  const [photoDataUrl, setPhotoDataUrl] = useState(initialData?.photoDataUrl || null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  // AI Classification State
  const [classification, setClassification] = useState(initialData?.classification || null);
  const [selectedMaterial, setSelectedMaterial] = useState(initialData?.material_name || '');
  const [correctionMade, setCorrectionMade] = useState(false);

  // Quality Assessment State
  const [ageYears, setAgeYears] = useState(1.5);
  const [damagePct, setDamagePct] = useState(8.0);
  const [originalUsage, setOriginalUsage] = useState('Commercial Demolition Salvage');
  const [qualityData, setQualityData] = useState(initialData?.qualityData || null);

  // Quantity & Units
  const [quantity, setQuantity] = useState(initialData?.quantity || 1000);
  const [unit, setUnit] = useState(initialData?.unit || 'Pieces');

  // Valuation
  const [valuationData, setValuationData] = useState(initialData?.valuationData || null);
  const [sellingPrice, setSellingPrice] = useState(initialData?.valuationData?.estimated_price || '');

  // Location & Details
  const [city, setCity] = useState(user?.city || 'Bangalore');
  const [state, setState] = useState(user?.state || 'Karnataka');
  const [availability, setAvailability] = useState('Immediate Pickup');

  // Publishing State
  const [publishing, setPublishing] = useState(false);
  const [publishSuccess, setPublishSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  // 1. Photo Capture Callback
  const handlePhotoCaptured = (dataUrl) => {
    setPhotoDataUrl(dataUrl);
    setSelectedFile(null);
    runAIAnalysis(dataUrl);
  };

  // 2. File Upload Callback
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setSelectedFile(file);

    const reader = new FileReader();
    reader.onload = (ev) => {
      const dataUrl = ev.target.result;
      setPhotoDataUrl(dataUrl);
      runAIAnalysis(dataUrl);
    };
    reader.readAsDataURL(file);
  };

  // 3. AI Computer Vision Pipeline
  const runAIAnalysis = async (dataUrl) => {
    setAnalyzing(true);
    setErrorMsg(null);
    setStep(2); // Jump to analysis screen

    try {
      const result = await api.predictMaterial(dataUrl);
      setClassification(result);
      setSelectedMaterial(result.predicted_material);

      // Auto-run preliminary quality & price
      const qRes = await api.assessQuality({
        material_name: result.predicted_material,
        age_years: ageYears,
        damage_percentage: damagePct,
        original_usage: originalUsage
      });
      setQualityData(qRes);

      const pRes = await api.predictPrice({
        material_name: result.predicted_material,
        quantity: quantity,
        unit: unit,
        quality_score: qRes.quality_score,
        age_years: ageYears,
        damage_percentage: damagePct,
        city: city
      });
      setValuationData(pRes);
      setSellingPrice(pRes.estimated_price);
    } catch (err) {
      console.error('AI Analysis failed:', err);
      setErrorMsg(err.message || 'Unable to analyze image. You can select material manually.');
    } finally {
      setAnalyzing(false);
    }
  };

  // Quality Recalculation
  const handleRecalculateQuality = async () => {
    try {
      const qRes = await api.assessQuality({
        material_name: selectedMaterial,
        age_years: parseFloat(ageYears),
        damage_percentage: parseFloat(damagePct),
        original_usage: originalUsage
      });
      setQualityData(qRes);

      const pRes = await api.predictPrice({
        material_name: selectedMaterial,
        quantity: parseFloat(quantity),
        unit: unit,
        quality_score: qRes.quality_score,
        age_years: parseFloat(ageYears),
        damage_percentage: parseFloat(damagePct),
        city: city
      });
      setValuationData(pRes);
      setSellingPrice(pRes.estimated_price);
    } catch (err) {
      console.error('Error recalculating:', err);
    }
  };

  // Submit Listing
  const handlePublishListing = async () => {
    if (!user) {
      alert('Please sign in or register to publish a listing.');
      onNavigate('login');
      return;
    }
    setPublishing(true);
    setErrorMsg(null);

    try {
      // Record feedback if user corrected material
      if (correctionMade && classification) {
        await api.submitFeedback({
          predicted_material: classification.predicted_material,
          corrected_material: selectedMaterial,
          predicted_quality: qualityData?.quality_grade,
          predicted_price: valuationData?.estimated_price,
          final_price: parseFloat(sellingPrice),
          confidence: classification.confidence,
          feedback_notes: "User verified and corrected material in 9-step wizard."
        }).catch(err => console.warn("Feedback log failed:", err));
      }

      await api.createListing({
        material_name: selectedMaterial,
        category: classification?.category || "General Construction",
        quantity: parseFloat(quantity),
        unit: unit,
        age_years: parseFloat(ageYears),
        damage_percentage: parseFloat(damagePct),
        price: parseFloat(sellingPrice),
        quality_grade: qualityData?.quality_grade || "B",
        quality_score: qualityData?.quality_score || 80.0,
        ai_confidence: classification?.confidence || 0.90,
        ai_estimated_price: valuationData?.estimated_price || parseFloat(sellingPrice),
        city: city,
        state: state,
        original_usage: originalUsage,
        availability: availability,
        image_url: photoDataUrl || "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=800&auto=format&fit=crop&q=60"
      });

      setPublishSuccess(true);
    } catch (err) {
      console.error("Listing publish failed:", err);
      setErrorMsg(err.message || "Failed to publish listing. Please try again.");
    } finally {
      setPublishing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Wizard Header Progress Tracker */}
      <div className="mb-8">
        <div className="flex items-center justify-between text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
          <span>Step {step} of 5</span>
          <span className="text-emerald-700 font-bold">
            {step === 1 && "Capture / Upload"}
            {step === 2 && "AI Material Identification"}
            {step === 3 && "Quality & Usability Grading"}
            {step === 4 && "Quantity & Valuation"}
            {step === 5 && "Review & Publish"}
          </span>
        </div>
        <div className="w-full bg-gray-200 h-2 rounded-full overflow-hidden">
          <div
            className="bg-emerald-600 h-full transition-all duration-300 rounded-full"
            style={{ width: `${(step / 5) * 100}%` }}
          />
        </div>
      </div>

      {errorMsg && (
        <div className="mb-6 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* STEP 1: CAPTURE OR UPLOAD */}
      {step === 1 && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <Camera className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Capture or Upload Material Photo</h2>
          <p className="text-gray-600 text-sm max-w-md mx-auto mb-8">
            REBUILD AI uses Computer Vision (MobileNetV2) to identify construction materials, assess quality, and compute circular valuations.
          </p>

          <div className="grid sm:grid-cols-2 gap-4 max-w-lg mx-auto">
            {/* Take Photo Option */}
            <button
              type="button"
              onClick={() => setCameraModalOpen(true)}
              className="flex flex-col items-center justify-center gap-3 p-6 rounded-2xl border-2 border-emerald-500 bg-emerald-50/50 hover:bg-emerald-50 text-emerald-800 transition group shadow-sm"
            >
              <div className="w-12 h-12 rounded-xl bg-emerald-600 text-white flex items-center justify-center group-hover:scale-105 transition">
                <Camera className="w-6 h-6" />
              </div>
              <span className="font-semibold text-sm">Take Photo with Camera</span>
              <span className="text-xs text-emerald-600">Supports mobile & desktop camera</span>
            </button>

            {/* Upload Image Option */}
            <label className="flex flex-col items-center justify-center gap-3 p-6 rounded-2xl border-2 border-gray-200 hover:border-gray-300 hover:bg-gray-50 text-gray-700 transition cursor-pointer group">
              <div className="w-12 h-12 rounded-xl bg-gray-100 text-gray-600 flex items-center justify-center group-hover:scale-105 transition">
                <Upload className="w-6 h-6" />
              </div>
              <span className="font-semibold text-sm">Upload Image File</span>
              <span className="text-xs text-gray-500">JPG, PNG, WEBP up to 25MB</span>
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleFileUpload}
                className="hidden"
              />
            </label>
          </div>
        </div>
      )}

      {/* STEP 2: AI MATERIAL IDENTIFICATION */}
      {step === 2 && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div>
              <span className="text-xs font-semibold text-emerald-600 uppercase tracking-wider">Input Preview</span>
              {photoDataUrl ? (
                <img src={photoDataUrl} alt="Captured material" className="mt-2 w-full h-64 object-cover rounded-xl border border-gray-200" />
              ) : (
                <div className="mt-2 w-full h-64 bg-gray-100 rounded-xl flex items-center justify-center text-gray-400">
                  No image available
                </div>
              )}
            </div>

            <div>
              {analyzing ? (
                <div className="text-center py-12">
                  <RefreshCw className="w-10 h-10 text-emerald-600 animate-spin mx-auto mb-4" />
                  <h3 className="text-lg font-bold text-gray-900 mb-1">Scanning Material with MobileNetV2...</h3>
                  <p className="text-gray-500 text-xs">Extracting 1280-dim feature vector and evaluating condition</p>
                </div>
              ) : classification ? (
                <div>
                  <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold mb-3">
                    <Sparkles className="w-3.5 h-3.5" />
                    AI Detection: {(classification.confidence * 100).toFixed(1)}% Confidence
                  </div>

                  <h3 className="text-2xl font-bold text-gray-900 mb-1">{classification.predicted_material}</h3>
                  <p className="text-sm text-gray-500 mb-4">Category: <span className="font-semibold text-gray-700">{classification.category}</span></p>

                  {/* Human-in-the-Loop Material Verification */}
                  <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 mb-6">
                    <label className="block text-xs font-semibold text-gray-700 mb-2">
                      Verify or Correct Detected Material:
                    </label>
                    <select
                      value={selectedMaterial}
                      onChange={(e) => {
                        setSelectedMaterial(e.target.value);
                        setCorrectionMade(true);
                      }}
                      className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-800 font-medium focus:ring-2 focus:ring-emerald-500 outline-none"
                    >
                      {MATERIAL_OPTIONS.map(m => (
                        <option key={m} value={m}>{m}</option>
                      ))}
                    </select>
                    {correctionMade && (
                      <p className="text-[11px] text-emerald-600 mt-1.5 flex items-center gap-1">
                        <Check className="w-3.5 h-3.5" /> Correction logged for model retraining feedback
                      </p>
                    )}
                  </div>

                  <button
                    type="button"
                    onClick={() => setStep(3)}
                    className="w-full flex items-center justify-center gap-2 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-xl transition shadow-md shadow-emerald-600/20"
                  >
                    Confirm & Proceed to Quality Grading
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              ) : (
                <div className="text-center py-6">
                  <p className="text-sm text-gray-600 mb-4">Select material manually to continue:</p>
                  <select
                    value={selectedMaterial}
                    onChange={(e) => setSelectedMaterial(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm mb-4"
                  >
                    {MATERIAL_OPTIONS.map(m => <option key={m} value={m}>{m}</option>)}
                  </select>
                  <button
                    type="button"
                    onClick={() => setStep(3)}
                    className="w-full py-2.5 bg-emerald-600 text-white rounded-xl text-sm font-semibold"
                  >
                    Continue
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* STEP 3: QUALITY ASSESSMENT */}
      {step === 3 && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
          <h2 className="text-xl font-bold text-gray-900 mb-2">Multimodal Quality & Condition Assessment</h2>
          <p className="text-gray-600 text-sm mb-6">
            Adjust material parameters to refine the 0–100 condition score and Grade A–E classification.
          </p>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">
                  Age of Material: {ageYears} Years
                </label>
                <input
                  type="range"
                  min="0.5"
                  max="15.0"
                  step="0.5"
                  value={ageYears}
                  onChange={(e) => setAgeYears(e.target.value)}
                  onMouseUp={handleRecalculateQuality}
                  className="w-full accent-emerald-600"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">
                  Observed Damage / Wear: {damagePct}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="70"
                  step="1"
                  value={damagePct}
                  onChange={(e) => setDamagePct(e.target.value)}
                  onMouseUp={handleRecalculateQuality}
                  className="w-full accent-emerald-600"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Original Usage Context</label>
                <select
                  value={originalUsage}
                  onChange={(e) => {
                    setOriginalUsage(e.target.value);
                    handleRecalculateQuality();
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white"
                >
                  <option value="Residential Demolition Salvage">Residential Demolition Salvage</option>
                  <option value="Commercial Interior Renovation">Commercial Interior Renovation</option>
                  <option value="Industrial Infrastructure Surplus">Industrial Infrastructure Surplus</option>
                  <option value="Warehouse Deconstruction">Warehouse Deconstruction</option>
                </select>
              </div>
            </div>

            {/* Quality Score Card */}
            {qualityData && (
              <div className="p-6 rounded-2xl bg-gray-50 border border-gray-200 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Quality Grade</span>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      qualityData.quality_grade === 'A' ? 'bg-emerald-100 text-emerald-800' :
                      qualityData.quality_grade === 'B' ? 'bg-blue-100 text-blue-800' :
                      qualityData.quality_grade === 'C' ? 'bg-amber-100 text-amber-800' : 'bg-red-100 text-red-800'
                    }`}>
                      Grade {qualityData.quality_grade} ({qualityData.quality_score}/100)
                    </span>
                  </div>
                  <h4 className="text-lg font-bold text-gray-900 mb-1">{qualityData.condition_name} Condition</h4>
                  <p className="text-xs text-gray-600 mb-4">{qualityData.condition_description}</p>

                  <div className="text-xs space-y-1.5">
                    <span className="font-semibold text-gray-800 block">Recommended Secondary Uses:</span>
                    {qualityData.recommended_reuse.slice(0, 3).map((r, i) => (
                      <div key={i} className="text-emerald-700 flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 flex-shrink-0" />
                        <span>{r}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <p className="text-[10px] text-gray-400 mt-4 italic border-t pt-2">{qualityData.disclaimer}</p>
              </div>
            )}
          </div>

          <div className="flex justify-between">
            <button
              type="button"
              onClick={() => setStep(2)}
              className="inline-flex items-center gap-2 px-5 py-2.5 border border-gray-300 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
            <button
              type="button"
              onClick={() => setStep(4)}
              className="inline-flex items-center gap-2 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-sm font-semibold transition"
            >
              Next: Pricing & Quantity <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 4: QUANTITY & PRICE VALUATION */}
      {step === 4 && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
          <h2 className="text-xl font-bold text-gray-900 mb-2">Quantity & Market Valuation</h2>
          <p className="text-gray-600 text-sm mb-6">
            Our Gradient Boosting Regressor ($R^2 = 0.935$) benchmarks regional second-market pricing.
          </p>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Quantity</label>
                <input
                  type="number"
                  min="1"
                  value={quantity}
                  onChange={(e) => {
                    setQuantity(e.target.value);
                    handleRecalculateQuality();
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Unit of Measure</label>
                <select
                  value={unit}
                  onChange={(e) => {
                    setUnit(e.target.value);
                    handleRecalculateQuality();
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white"
                >
                  <option value="Pieces">Pieces</option>
                  <option value="Tonnes">Tonnes</option>
                  <option value="Sq.Ft">Sq.Ft</option>
                  <option value="Meters">Meters</option>
                  <option value="Kg">Kg</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Location (City)</label>
                <input
                  type="text"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Your Listing Selling Price (₹)</label>
                <input
                  type="number"
                  value={sellingPrice}
                  onChange={(e) => setSellingPrice(e.target.value)}
                  className="w-full px-3 py-2 border-2 border-emerald-500 rounded-lg text-lg font-bold text-emerald-900 bg-emerald-50/30"
                />
              </div>
            </div>

            {/* AI Valuation Card */}
            {valuationData && (
              <div className="p-6 rounded-2xl bg-emerald-50/50 border border-emerald-200 flex flex-col justify-between">
                <div>
                  <span className="text-xs font-bold text-emerald-800 uppercase tracking-wider">AI Valuation Suggestion</span>
                  <div className="mt-2 text-3xl font-extrabold text-emerald-900">
                    ₹{valuationData.estimated_price.toLocaleString()}
                  </div>
                  <p className="text-xs text-emerald-700 mt-1">
                    Rate: <b>₹{valuationData.price_per_unit.toFixed(2)}</b> / {valuationData.unit}
                  </p>

                  <div className="mt-4 p-3 bg-white rounded-xl border border-emerald-100 text-xs space-y-1 text-gray-700">
                    <p><b>Recommended Range:</b> ₹{valuationData.price_range_min.toLocaleString()} – ₹{valuationData.price_range_max.toLocaleString()}</p>
                    <p><b>Virgin Material Savings:</b> {valuationData.savings_percentage}% discount</p>
                    <p className="text-[11px] text-gray-500">ML Model: {valuationData.model_name} (Benchmark R² = 0.935)</p>
                  </div>
                </div>

                <div className="mt-4 text-xs text-emerald-800 flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-emerald-600" />
                  <span>Fair market rate helps sell inventory 3x faster</span>
                </div>
              </div>
            )}
          </div>

          <div className="flex justify-between">
            <button
              type="button"
              onClick={() => setStep(3)}
              className="inline-flex items-center gap-2 px-5 py-2.5 border border-gray-300 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
            <button
              type="button"
              onClick={() => setStep(5)}
              className="inline-flex items-center gap-2 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-sm font-semibold transition"
            >
              Review Complete Listing <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 5: REVIEW & PUBLISH */}
      {step === 5 && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
          {publishSuccess ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="w-10 h-10" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Listing Published Successfully!</h2>
              <p className="text-gray-600 text-sm max-w-md mx-auto mb-6">
                Your material is now discoverable on the REBUILD AI marketplace and open for buyer negotiation offers.
              </p>
              <div className="flex justify-center gap-3">
                <button
                  onClick={() => onNavigate('marketplace')}
                  className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-xl transition"
                >
                  View in Marketplace
                </button>
                <button
                  onClick={() => {
                    setStep(1);
                    setPublishSuccess(false);
                    setPhotoDataUrl(null);
                  }}
                  className="px-6 py-2.5 border border-gray-300 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  List Another Material
                </button>
              </div>
            </div>
          ) : (
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Review & Publish Listing</h2>
              <p className="text-gray-600 text-sm mb-6">
                Verify all parameters before broadcasting your listing to contractors and builders.
              </p>

              <div className="grid md:grid-cols-2 gap-6 mb-8">
                {photoDataUrl && (
                  <img src={photoDataUrl} alt="Listing preview" className="w-full h-64 object-cover rounded-xl border border-gray-200" />
                )}
                <div className="space-y-2 text-sm text-gray-700">
                  <div className="p-4 bg-gray-50 rounded-xl space-y-2">
                    <p><b>Material:</b> {selectedMaterial}</p>
                    <p><b>Grade:</b> Grade {qualityData?.quality_grade} ({qualityData?.quality_score}/100)</p>
                    <p><b>Quantity:</b> {quantity} {unit}</p>
                    <p><b>Selling Price:</b> ₹{parseFloat(sellingPrice || 0).toLocaleString()}</p>
                    <p><b>Location:</b> {city}, {state}</p>
                    <p><b>Availability:</b> {availability}</p>
                  </div>

                  {/* Circular LCA Preview */}
                  <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-200">
                    <span className="text-xs font-bold text-emerald-800 flex items-center gap-1.5 mb-1">
                      <Leaf className="w-4 h-4 text-emerald-600" />
                      Circular Environmental Benefit:
                    </span>
                    <p className="text-xs text-emerald-900">
                      Estimated Landfill Diversion: <b>{((parseFloat(quantity) * 3) / 1000).toFixed(2)} tonnes</b>
                    </p>
                    <p className="text-xs text-emerald-900">
                      Estimated Avoided Carbon: <b>{((parseFloat(quantity) * 0.7)).toFixed(0)} kg CO₂e</b>
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex justify-between">
                <button
                  type="button"
                  onClick={() => setStep(4)}
                  className="inline-flex items-center gap-2 px-5 py-2.5 border border-gray-300 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  <ArrowLeft className="w-4 h-4" /> Back
                </button>
                <button
                  type="button"
                  onClick={handlePublishListing}
                  disabled={publishing}
                  className="inline-flex items-center gap-2 px-8 py-3 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white rounded-xl font-bold shadow-lg shadow-emerald-600/25 transition"
                >
                  {publishing ? 'Publishing to Marketplace...' : 'Publish Listing Now'}
                  <CheckCircle2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Real Device Camera Modal */}
      <CameraCaptureModal
        isOpen={cameraModalOpen}
        onClose={() => setCameraModalOpen(false)}
        onPhotoCaptured={handlePhotoCaptured}
      />
    </div>
  );
}
