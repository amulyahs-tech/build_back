import os
import sys
import io
import streamlit as st
from PIL import Image

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app.ml.material_classifier import material_classifier, MATERIAL_CLASSES
from backend.app.ml.quality_classifier import quality_classifier
from backend.app.ml.price_predictor import price_predictor, BASE_MARKET_RATES, CITY_DEMAND_INDEX
from backend.app.ml.environmental_calculator import calculate_environmental_impact
from backend.app.database import SessionLocal, Base, engine
from backend.app.models import Listing

try:
    from scripts.seed_database import seed_if_empty
except Exception:
    def seed_if_empty(db):
        pass


# Streamlit Page Setup
st.set_page_config(
    page_title="BuildBack – Construction Circular Economy",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-seed database if fresh
try:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db_session:
        seed_if_empty(db_session)
except Exception:
    pass

# Custom CSS for polished sustainability aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #065f46;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .metric-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-grade-A { background-color: #d1fae5; color: #065f46; }
    .badge-grade-B { background-color: #dbeafe; color: #1e40af; }
    .badge-grade-C { background-color: #fef3c7; color: #92400e; }
    .badge-grade-D { background-color: #fee2e2; color: #991b1b; }
    .badge-grade-E { background-color: #f3f4f6; color: #374151; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/recycle-sign.png", width=64)
st.sidebar.title("BuildBack")
st.sidebar.caption("AI-Powered Construction Waste Reuse & Second-Market Platform")

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "📸 AI Material Assessment",
        "🛒 Construction Waste Marketplace",
        "💰 AI Price Estimator",
        "🌱 Circular LCA Calculator",
        "ℹ️ About BuildBack & Architecture"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Platform Capabilities:**
* 🎯 20 Construction Material Classes
* 📷 Live Camera & Upload Support
* 🏆 A–E Multimodal Quality Grading
* 📈 Gradient Boosting Regressor ($R^2=0.935$)
* 🌍 Circular LCA Carbon Diverted Tracker
""")

# ==============================================================================
# PAGE 1: MATERIAL ANALYZER
# ==============================================================================
if nav_choice == "📸 AI Material Assessment":
    st.markdown('<div class="main-header">📸 AI Material Identification & Quality Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Take a real-time photo using your device camera or upload an existing site photograph.</div>', unsafe_allow_html=True)

    input_method = st.radio("Choose Input Method:", ["Take Photo with Camera", "Upload Image File"], horizontal=True)

    image_bytes = None

    if input_method == "Take Photo with Camera":
        camera_photo = st.camera_input("Point camera directly at the material in good lighting")
        if camera_photo is not None:
            image_bytes = camera_photo.getvalue()
    else:
        uploaded_file = st.file_uploader("Upload material photo (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])
        if uploaded_file is not None:
            image_bytes = uploaded_file.getvalue()

    if image_bytes:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(image_bytes, caption="Input Material Photo", use_container_width=True)

        with col2:
            st.subheader("Analysis Parameters")
            est_age = st.slider("Estimated Age (Years)", min_value=0.0, max_value=20.0, value=1.5, step=0.5)
            est_damage = st.slider("Observed Damage / Wear (%)", min_value=0.0, max_value=100.0, value=8.0, step=1.0)
            est_quantity = st.number_input("Estimated Quantity", min_value=1.0, value=1500.0, step=50.0)

            run_analysis = st.button("🚀 Analyze Material & Value", type="primary")

        if run_analysis:
            with st.spinner("Processing Computer Vision & Valuation Pipelines..."):
                # 1. Computer Vision Material Classification
                cv_result = material_classifier.predict(image_bytes)
                predicted_mat = cv_result["predicted_material"]
                conf = cv_result["confidence"]

                # 2. Quality Assessment
                q_result = quality_classifier.assess_quality(
                    material_name=predicted_mat,
                    age_years=est_age,
                    damage_percentage=est_damage
                )

                # 3. Price Prediction
                rate_info = BASE_MARKET_RATES.get(predicted_mat, {"unit": "Units"})
                p_result = price_predictor.predict_price(
                    material_name=predicted_mat,
                    quantity=est_quantity,
                    unit=rate_info.get("unit", "Units"),
                    quality_score=q_result["quality_score"],
                    age_years=est_age,
                    damage_percentage=est_damage,
                    city="Bangalore"
                )

                # 4. LCA Environmental Impact
                env_result = calculate_environmental_impact(
                    material_name=predicted_mat,
                    quantity=est_quantity,
                    unit=rate_info.get("unit", "Units")
                )

            st.markdown("---")
            st.success("✅ Analysis Complete")

            # Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Identified Material", predicted_mat, f"{conf * 100:.1f}% Confidence")
            m2.metric("Quality Grade", f"Grade {q_result['quality_grade']}", f"{q_result['quality_score']}/100 Score")
            m3.metric("Estimated Market Value", f"₹{p_result['estimated_price']:,.0f}", f"₹{p_result['price_per_unit']:.1f} / {p_result['unit']}")
            m4.metric("Avoided Carbon", f"{env_result['estimated_co2_saving_kg']:,} kg CO₂e", f"{env_result['estimated_weight_tonnes']} tonnes diverted")

            # Deep Breakdown Tabs
            t1, t2, t3, t4 = st.tabs(["📋 Material Details", "🏆 Quality & Usability", "💰 Valuation Breakdown", "🌱 Environmental LCA"])

            with t1:
                st.write(f"**Primary Classification:** {predicted_mat}")
                st.write(f"**Category:** {cv_result['category']}")
                st.write(f"**Circularity Tier:** {cv_result['recyclability_tier']}")
                if cv_result["low_confidence_warning"]:
                    st.warning("⚠️ Low confidence detected (<70%). Consider retaking photo under better lighting.")

                st.write("**Top Visual Alternative Predictions:**")
                for alt in cv_result["top_predictions"]:
                    st.write(f"* {alt['material']}: `{alt['confidence'] * 100:.1f}%`")

            with t2:
                st.write(f"**Condition Assessment:** {q_result['condition_name']}")
                st.write(f"*{q_result['condition_description']}*")
                st.write("**Recommended Secondary Uses:**")
                for use in q_result["recommended_reuse"]:
                    st.write(f"✓ {use}")
                st.write("**Unsuitable Applications:**")
                for un in q_result["unsuitable_uses"]:
                    st.write(f"✗ {un}")
                st.caption(q_result["disclaimer"])

            with t3:
                st.write(f"**Fair Market Second-Hand Rate:** ₹{p_result['price_per_unit']:.2f} per {p_result['unit']}")
                st.write(f"**Estimated Valuation:** ₹{p_result['estimated_price']:,.0f}")
                st.write(f"**Negotiation Range:** ₹{p_result['price_range_min']:,.0f} – ₹{p_result['price_range_max']:,.0f}")
                st.write(f"**Savings vs Brand New Virgin Material:** {p_result['savings_percentage']}% discount")
                st.caption(f"Engine: {p_result['model_name']} (Benchmark R²: {p_result['model_r2_benchmark']})")

            with t4:
                st.write(f"**Landfill Diverted Weight:** {env_result['estimated_weight_tonnes']} metric tonnes")
                st.write(f"**Embodied Carbon Avoided:** {env_result['estimated_co2_saving_kg']:,} kg CO₂e")
                st.write(f"**Virgin Raw Material Preserved:** {env_result['virgin_material_preserved_kg']:,} kg")
                st.write(f"**Tree Equivalent Absorption:** ~{env_result['trees_equivalent']} mature trees planted")
                st.caption(env_result["disclaimer"])

# ==============================================================================
# PAGE 2: MARKETPLACE LISTINGS
# ==============================================================================
elif nav_choice == "🛒 Construction Waste Marketplace":
    st.markdown('<div class="main-header">🛒 Construction Material Marketplace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Browse verified surplus and reclaimed construction inventory across Indian cities.</div>', unsafe_allow_html=True)

    with SessionLocal() as db:
        listings = db.query(Listing).filter(Listing.status == "active").all()

    if listings:
        filter_col1, filter_col2 = st.columns([2, 1])
        with filter_col1:
            selected_cat = st.selectbox("Filter by Category", ["All Categories"] + sorted(list(set(l.category for l in listings))))
        with filter_col2:
            selected_grade = st.selectbox("Filter by Quality Grade", ["All Grades", "A", "B", "C", "D", "E"])

        filtered = [
            l for l in listings
            if (selected_cat == "All Categories" or l.category == selected_cat)
            and (selected_grade == "All Grades" or l.quality_grade == selected_grade)
        ]

        st.write(f"Showing **{len(filtered)}** active listings")

        cols = st.columns(3)
        for idx, item in enumerate(filtered):
            col = cols[idx % 3]
            with col:
                st.markdown(f"""
                <div class="card">
                    <img src="{item.image_url}" style="width:100%; height:160px; object-fit:cover; border-radius:6px; margin-bottom:0.8rem;"/>
                    <h4 style="margin:0 0 0.2rem 0; color:#0f172a;">{item.material_name}</h4>
                    <p style="color:#64748b; font-size:0.85rem; margin-bottom:0.5rem;">📍 {item.city}, {item.state}</p>
                    <div style="margin-bottom:0.6rem;">
                        <span class="metric-badge badge-grade-{item.quality_grade}">Grade {item.quality_grade} ({item.quality_score:.0f}/100)</span>
                    </div>
                    <p style="font-size:1.1rem; font-weight:700; color:#065f46; margin:0 0 0.2rem 0;">₹{item.price:,.0f}</p>
                    <p style="font-size:0.85rem; color:#475569; margin:0;">Quantity: <b>{item.quantity:,.0f} {item.unit}</b></p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No active marketplace listings found. Database seeding initialized.")

# ==============================================================================
# PAGE 3: PRICE ESTIMATOR
# ==============================================================================
elif nav_choice == "💰 AI Price Estimator":
    st.markdown('<div class="main-header">💰 Second-Market Price Valuation Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Predict fair secondary market pricing using our trained Gradient Boosting Regressor (R² = 0.935).</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mat_select = st.selectbox("Material Type", MATERIAL_CLASSES)
        quantity_input = st.number_input("Quantity", min_value=1.0, value=1000.0, step=10.0)
        city_select = st.selectbox("Regional Market City", list(CITY_DEMAND_INDEX.keys()))

    with col2:
        quality_score_input = st.slider("Material Quality Condition (0 = Scrap, 100 = Like New)", 0.0, 100.0, 82.0, 1.0)
        age_input = st.slider("Material Age (Years)", 0.0, 15.0, 1.5, 0.5)
        damage_input = st.slider("Observed Damage / Wear (%)", 0.0, 100.0, 10.0, 1.0)

    rate_info = BASE_MARKET_RATES.get(mat_select, {"unit": "Units"})
    valuation = price_predictor.predict_price(
        material_name=mat_select,
        quantity=quantity_input,
        unit=rate_info.get("unit", "Units"),
        quality_score=quality_score_input,
        age_years=age_input,
        damage_percentage=damage_input,
        city=city_select
    )

    st.markdown("---")
    res1, res2, res3 = st.columns(3)
    res1.metric("Predicted Total Price", f"₹{valuation['estimated_price']:,.0f}")
    res2.metric("Negotiation Window", f"₹{valuation['price_range_min']:,.0f} – ₹{valuation['price_range_max']:,.0f}")
    res3.metric(f"Rate per {valuation['unit']}", f"₹{valuation['price_per_unit']:.2f}", f"{valuation['savings_percentage']}% vs virgin")

# ==============================================================================
# PAGE 4: ENVIRONMENTAL CALCULATOR
# ==============================================================================
elif nav_choice == "🌱 Circular LCA Calculator":
    st.markdown('<div class="main-header">🌱 Circular LCA & Embodied Carbon Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Calculate avoided embodied carbon and diverted landfill mass based on lifecycle assessment data.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        calc_mat = st.selectbox("Select Construction Material", MATERIAL_CLASSES)
    with c2:
        calc_qty = st.number_input("Quantity Diverted / Reused", min_value=1.0, value=2500.0, step=100.0)

    rate_info = BASE_MARKET_RATES.get(calc_mat, {"unit": "Pieces"})
    impact = calculate_environmental_impact(calc_mat, calc_qty, rate_info.get("unit", "Pieces"))

    st.markdown("---")
    e1, e2, e3 = st.columns(3)
    e1.metric("Landfill Diversion", f"{impact['estimated_weight_tonnes']:,} Tonnes")
    e2.metric("Avoided Carbon (Embodied)", f"{impact['estimated_co2_saving_kg']:,} kg CO₂e")
    e3.metric("Sequestration Equivalent", f"{impact['trees_equivalent']} Mature Trees")

    st.info(f"Preserving approximately **{impact['virgin_material_preserved_kg']:,} kg** of virgin raw quarry/mine extraction resources.")
    st.caption(impact["disclaimer"])

# ==============================================================================
# PAGE 5: ABOUT & TECHNOLOGY
# ==============================================================================
elif nav_choice == "ℹ️ About BuildBack & Architecture":
    st.markdown('<div class="main-header">ℹ️ About REBUILD AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Revolutionizing the construction circular economy through Computer Vision and Machine Learning.</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🏗️ Problem Statement
    The construction and demolition (C&D) industry produces millions of tonnes of scrap annually. Materials like clay bricks,
    TMT rebar, structural timber, and aggregates can be safely salvaged, but second-hand adoption remains low due to:
    * Absence of standardized, transparent quality grading
    * Subjective, arbitrary pricing benchmarks
    * High friction in cataloging and material identification
    * Lack of certified environmental quantification for ESG / carbon credits

    ### 🧠 Technology Stack & Methodology
    * **Computer Vision**: MobileNetV2 feature extractor trained across 20 primary construction material classes.
    * **Quality Grading**: A–E standard quality classification matching 0–100 numerical degradation metrics.
    * **Price Prediction**: Multi-feature Gradient Boosting Regressor achieving $R^2 = 0.935$ against empirical market pricing.
    * **Visual Similarity**: 1280-dimensional cosine similarity search across active listings.
    * **Circular LCA**: Embodied carbon savings modeling derived from the ICE Bath Inventory of Carbon & Energy.
    """)
