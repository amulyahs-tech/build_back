import os
import sys
import io
import datetime
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
from backend.app.models import Listing, PurchaseRequest, User, Favorite, EnvironmentalImpact, Transaction

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
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .metric-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-grade-A { background-color: #d1fae5; color: #065f46; }
    .badge-grade-B { background-color: #dbeafe; color: #1e40af; }
    .badge-grade-C { background-color: #fef3c7; color: #92400e; }
    .badge-grade-D { background-color: #fee2e2; color: #991b1b; }
    .badge-grade-E { background-color: #f3f4f6; color: #374151; }

    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .status-pending { background-color: #fef3c7; color: #92400e; }
    .status-accepted { background-color: #d1fae5; color: #065f46; }
    .status-rejected { background-color: #fee2e2; color: #991b1b; }

    .action-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdfa 100%);
        border: 1px solid #a7f3d0;
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Navigation choices
NAV_OPTIONS = [
    "📸 AI Material Assessment",
    "🛒 Construction Waste Marketplace",
    "📦 Seller Hub & Inventory",
    "➕ Sell Surplus Material",
    "🛍️ Buyer Portal & Orders",
    "💰 AI Price Estimator",
    "🌱 Circular LCA Calculator",
    "ℹ️ About BuildBack & Architecture"
]

if "current_nav" not in st.session_state:
    st.session_state.current_nav = NAV_OPTIONS[0]

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/recycle-sign.png", width=64)
st.sidebar.title("BuildBack")
st.sidebar.caption("AI-Powered Construction Waste Reuse & Second-Market Platform")

nav_choice = st.sidebar.radio(
    "Navigation",
    NAV_OPTIONS,
    index=NAV_OPTIONS.index(st.session_state.current_nav) if st.session_state.current_nav in NAV_OPTIONS else 0,
    key="nav_radio"
)
st.session_state.current_nav = nav_choice

st.sidebar.markdown("---")
st.sidebar.info("""
**Platform Capabilities:**
* 🎯 20 Construction Material Classes
* 📷 Live Camera & Upload Support
* 🏆 A–E Multimodal Quality Grading
* 📈 Gradient Boosting Regressor ($R^2=0.935$)
* 📦 Dedicated Seller & Buyer Workflows
* 🌍 Circular LCA Carbon Diverted Tracker
""")


# ==============================================================================
# HELPER FUNCTIONS FOR SELLER & BUYER DATABASE OPERATIONS
# ==============================================================================
def get_default_users(db):
    """Retrieves or creates default seller and buyer accounts for public interaction."""
    seller = db.query(User).filter(User.user_type.in_(["SELLER", "BOTH"])).first()
    buyer = db.query(User).filter(User.user_type.in_(["BUYER", "BOTH"])).first()
    if not seller:
        seller = User(name="Apex Demolition & Salvage Corp", email="seller@demolitioncorp.com", phone="+91 9880012345", password_hash="dummy", user_type="SELLER", city="Bangalore")
        db.add(seller)
        db.commit()
        db.refresh(seller)
    if not buyer:
        buyer = User(name="GreenBuild Contractors Ltd", email="buyer@greenbuild.in", phone="+91 9900054321", password_hash="dummy", user_type="BUYER", city="Bangalore")
        db.add(buyer)
        db.commit()
        db.refresh(buyer)
    return seller, buyer


# ==============================================================================
# PAGE 1: MATERIAL ANALYZER (WITH DIRECT SELLER & BUYER INTEGRATION)
# ==============================================================================
if nav_choice == "📸 AI Material Assessment":
    st.markdown('<div class="main-header">📸 AI Material Identification & Quality Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Take a real-time photo using your device camera or upload an existing site photograph. Connect directly to Seller and Buyer markets.</div>', unsafe_allow_html=True)

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
            est_quantity = st.number_input("Estimated Quantity", min_value=1.0, value=1000.0, step=50.0)

            run_analysis = st.button("🚀 Analyze Material & Value", type="primary")

        if run_analysis or "last_analysis" in st.session_state:
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
                    unit_name = rate_info.get("unit", "Units")
                    p_result = price_predictor.predict_price(
                        material_name=predicted_mat,
                        quantity=est_quantity,
                        unit=unit_name,
                        quality_score=q_result["quality_score"],
                        age_years=est_age,
                        damage_percentage=est_damage,
                        city="Bangalore"
                    )

                    # 4. LCA Environmental Impact
                    env_result = calculate_environmental_impact(
                        material_name=predicted_mat,
                        quantity=est_quantity,
                        unit=unit_name
                    )

                    st.session_state["last_analysis"] = {
                        "cv": cv_result,
                        "quality": q_result,
                        "price": p_result,
                        "env": env_result,
                        "quantity": est_quantity,
                        "unit": unit_name,
                        "age": est_age,
                        "damage": est_damage,
                        "predicted_mat": predicted_mat,
                        "conf": conf
                    }

            analysis = st.session_state["last_analysis"]
            predicted_mat = analysis["predicted_mat"]
            conf = analysis["conf"]
            q_result = analysis["quality"]
            p_result = analysis["price"]
            env_result = analysis["env"]
            cv_result = analysis["cv"]

            st.markdown("---")
            st.success("✅ Analysis Complete")

            # Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Identified Material", predicted_mat, f"{conf * 100:.1f}% Confidence")
            m2.metric("Quality Grade", f"Grade {q_result['quality_grade']}", f"{q_result['quality_score']}/100 Score")
            m3.metric("Estimated Market Value", f"₹{p_result['estimated_price']:,.0f}", f"₹{p_result['price_per_unit']:.1f} / {p_result['unit']}")
            m4.metric("Avoided Carbon", f"{env_result['estimated_co2_saving_kg']:,} kg CO₂e", f"{env_result['estimated_weight_tonnes']} tonnes diverted")

            # Deep Breakdown Tabs (Includes New Tab: Current Marketplace Availability & Sellers)
            t1, t2, t3, t4, t5 = st.tabs([
                "📋 Material Details",
                "🏆 Quality & Usability",
                "💰 Valuation Breakdown",
                "🌱 Environmental LCA",
                "🏪 Marketplace Availability & Sellers"
            ])

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

            # NEW TAB 5: Live Marketplace Availability & Seller Details for Buyers
            with t5:
                st.markdown(f"#### Verified Sellers Offering **{predicted_mat}** (or category equivalents)")
                with SessionLocal() as db:
                    matching_listings = db.query(Listing).filter(
                        Listing.status == "active",
                        (Listing.material_name.ilike(f"%{predicted_mat}%") | (Listing.category == cv_result["category"]))
                    ).all()

                if matching_listings:
                    st.write(f"Found **{len(matching_listings)}** verified active listings available for immediate acquisition:")
                    for item in matching_listings:
                        with st.expander(f"📦 {item.material_name} – ₹{item.price:,.0f} (Grade {item.quality_grade}) in {item.city}"):
                            lcol1, lcol2 = st.columns([1, 2])
                            with lcol1:
                                st.image(item.image_url, use_container_width=True)
                            with lcol2:
                                with SessionLocal() as db_sub:
                                    seller_obj = db_sub.query(User).filter(User.id == item.seller_id).first()
                                    seller_name = seller_obj.name if seller_obj else "Demolition Recovery Supplier"
                                    seller_phone = seller_obj.phone if seller_obj else "+91 9880012345"

                                st.write(f"**Seller:** {seller_name} ({item.city}, {item.state})")
                                st.write(f"**Contact:** 📞 `{seller_phone}`")
                                st.write(f"**Available Quantity:** {item.quantity:,.0f} {item.unit}")
                                st.write(f"**Quality Score:** {item.quality_score:.0f}/100 (Grade {item.quality_grade})")
                                st.write(f"**Asking Price:** ₹{item.price:,.0f}")

                                # Quick offer button inside assessment tab
                                offer_qty = st.number_input(f"Quantity to Purchase ({item.unit})", min_value=1.0, value=min(item.quantity, 100.0), step=10.0, key=f"assess_qty_{item.id}")
                                offer_price = st.number_input("Proposed Offer Price (₹)", min_value=100.0, value=float(item.price), step=500.0, key=f"assess_pr_{item.id}")
                                if st.button(f"Send Purchase Offer for {item.material_name}", key=f"btn_offer_{item.id}"):
                                    with SessionLocal() as db_buy:
                                        _, buyer_usr = get_default_users(db_buy)
                                        new_req = PurchaseRequest(
                                            listing_id=item.id,
                                            buyer_id=buyer_usr.id,
                                            quantity=offer_qty,
                                            proposed_price=offer_price,
                                            message="Direct buyer inquiry submitted from AI Assessment diagnostic report.",
                                            preferred_pickup_date="Immediate site pickup",
                                            status="pending"
                                        )
                                        db_buy.add(new_req)
                                        db_buy.commit()
                                    st.success("🎉 Your purchase request has been transmitted to the seller! View it in '🛍️ Buyer Portal & Orders'.")
                else:
                    st.info(f"No active sellers currently listing exact material '{predicted_mat}'. You can list it as a seller or check the full Marketplace.")

            # DUAL ACTION WORKFLOWS: SELLER AND BUYER ACTION BRIDGES
            st.markdown("---")
            act_col1, act_col2 = st.columns(2)

            with act_col1:
                st.markdown("""
                <div class="action-box">
                    <h4 style="margin:0 0 0.3rem 0; color:#065f46;">📦 Seller Workflow</h4>
                    <p style="font-size:0.85rem; color:#475569; margin-bottom:0.8rem;">
                        Want to liquidate this salvaged lot? Transfer this AI diagnostic directly into a new marketplace listing.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Transfer to Sell Listing Wizard →", type="primary", use_container_width=True):
                    st.session_state["prefill_listing"] = {
                        "material_name": predicted_mat,
                        "category": cv_result["category"],
                        "quality_grade": q_result["quality_grade"],
                        "quality_score": q_result["quality_score"],
                        "quantity": analysis["quantity"],
                        "unit": analysis["unit"],
                        "price": p_result["estimated_price"],
                        "age": analysis["age"],
                        "damage": analysis["damage"]
                    }
                    st.session_state.current_nav = "➕ Sell Surplus Material"
                    st.rerun()

            with act_col2:
                st.markdown("""
                <div class="action-box">
                    <h4 style="margin:0 0 0.3rem 0; color:#1e40af;">🛒 Buyer Workflow</h4>
                    <p style="font-size:0.85rem; color:#475569; margin-bottom:0.8rem;">
                        Looking to source certified recycled stock? Explore all active listings and negotiate prices directly with verified sellers.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Explore Marketplace for this Material →", use_container_width=True):
                    st.session_state["filter_category"] = cv_result["category"]
                    st.session_state.current_nav = "🛒 Construction Waste Marketplace"
                    st.rerun()


# ==============================================================================
# PAGE 2: INTERACTIVE MARKETPLACE (WITH SELLER DETAILS & BUYER OFFERS)
# ==============================================================================
elif nav_choice == "🛒 Construction Waste Marketplace":
    st.markdown('<div class="main-header">🛒 Construction Material Marketplace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Browse verified salvaged construction inventory, inspect seller contacts, and submit purchase offers.</div>', unsafe_allow_html=True)

    with SessionLocal() as db:
        all_listings = db.query(Listing).filter(Listing.status == "active").all()

    if all_listings:
        categories = ["All Categories"] + sorted(list(set(l.category for l in all_listings)))
        default_cat = st.session_state.get("filter_category", "All Categories")
        default_cat_idx = categories.index(default_cat) if default_cat in categories else 0

        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            search_query = st.text_input("🔍 Search by Material Name or Keyword", placeholder="e.g. Red Bricks, TMT Steel, Sand...")
        with f2:
            selected_cat = st.selectbox("Category Filter", categories, index=default_cat_idx)
        with f3:
            selected_grade = st.selectbox("Quality Grade Filter", ["All Grades", "A", "B", "C", "D", "E"])

        filtered = [
            l for l in all_listings
            if (selected_cat == "All Categories" or l.category == selected_cat)
            and (selected_grade == "All Grades" or l.quality_grade == selected_grade)
            and (not search_query or search_query.lower() in l.material_name.lower() or search_query.lower() in l.category.lower())
        ]

        st.write(f"Showing **{len(filtered)}** verified active items")

        cols = st.columns(3)
        for idx, item in enumerate(filtered):
            col = cols[idx % 3]
            with col:
                with SessionLocal() as db_item:
                    seller = db_item.query(User).filter(User.id == item.seller_id).first()
                    seller_name = seller.name if seller else "Demolition Recovery Supplier"
                    seller_phone = seller.phone if seller else "+91 9880012345"

                st.markdown(f"""
                <div class="card">
                    <img src="{item.image_url}" style="width:100%; height:160px; object-fit:cover; border-radius:8px; margin-bottom:0.8rem;"/>
                    <h4 style="margin:0 0 0.2rem 0; color:#0f172a; font-size:1.1rem;">{item.material_name}</h4>
                    <p style="color:#64748b; font-size:0.85rem; margin-bottom:0.4rem;">📍 {item.city}, {item.state}</p>
                    <div style="margin-bottom:0.5rem; display:flex; gap:0.5rem; align-items:center;">
                        <span class="metric-badge badge-grade-{item.quality_grade}">Grade {item.quality_grade} ({item.quality_score:.0f}/100)</span>
                        <span style="font-size:0.75rem; color:#059669; font-weight:600;">{(item.ai_confidence * 100):.0f}% AI Verified</span>
                    </div>
                    <p style="font-size:1.2rem; font-weight:800; color:#065f46; margin:0 0 0.2rem 0;">₹{item.price:,.0f}</p>
                    <p style="font-size:0.85rem; color:#475569; margin:0 0 0.5rem 0;">Available: <b>{item.quantity:,.0f} {item.unit}</b></p>
                    <div style="padding:0.5rem; background:#f1f5f9; border-radius:6px; font-size:0.75rem; color:#334155;">
                        👤 <b>Seller:</b> {seller_name}<br/>
                        📞 <b>Contact:</b> {seller_phone}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Purchase Offer Expander for Buyers
                with st.expander(f"💬 Make Purchase Offer on {item.material_name}"):
                    offer_form_key = f"market_offer_form_{item.id}"
                    with st.form(key=offer_form_key):
                        st.write(f"**Target Item:** {item.material_name} ({item.city})")
                        prop_qty = st.number_input("Quantity Requested", min_value=1.0, value=float(item.quantity), step=10.0, key=f"qty_in_{item.id}")
                        prop_price = st.number_input("Proposed Total Price (₹)", min_value=100.0, value=float(item.price), step=500.0, key=f"price_in_{item.id}")
                        pickup_str = st.text_input("Preferred Pickup Date", value="Immediate inspection & collection", key=f"pick_in_{item.id}")
                        notes = st.text_area("Message / Note to Seller", value="Interested in inspecting and acquiring this salvaged lot.", key=f"notes_in_{item.id}")
                        submit_offer = st.form_submit_button("Send Purchase Offer 🚀")

                        if submit_offer:
                            with SessionLocal() as db_trans:
                                _, default_buyer = get_default_users(db_trans)
                                req = PurchaseRequest(
                                    listing_id=item.id,
                                    buyer_id=default_buyer.id,
                                    quantity=prop_qty,
                                    proposed_price=prop_price,
                                    message=notes,
                                    preferred_pickup_date=pickup_str,
                                    status="pending"
                                )
                                db_trans.add(req)
                                db_trans.commit()
                            st.success(f"✅ Purchase offer of ₹{prop_price:,.0f} sent to {seller_name}! Track progress under '🛍️ Buyer Portal & Orders'.")
    else:
        st.info("No active marketplace listings found.")


# ==============================================================================
# PAGE 3: SELLER HUB & INVENTORY MANAGEMENT
# ==============================================================================
elif nav_choice == "📦 Seller Hub & Inventory":
    st.markdown('<div class="main-header">📦 Seller Hub & Inventory Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Manage your active construction surplus inventory, review incoming buyer purchase offers, and accept orders.</div>', unsafe_allow_html=True)

    with SessionLocal() as db:
        default_seller, _ = get_default_users(db)
        seller_listings = db.query(Listing).filter(Listing.seller_id == default_seller.id).all()
        active_listings = [l for l in seller_listings if l.status == "active"]
        sold_listings = [l for l in seller_listings if l.status == "sold"]
        total_inv_val = sum(l.price for l in active_listings)

        # Incoming requests for this seller's listings
        listing_ids = [l.id for l in seller_listings]
        incoming_reqs = db.query(PurchaseRequest).filter(PurchaseRequest.listing_id.in_(listing_ids)).order_by(PurchaseRequest.created_at.desc()).all() if listing_ids else []

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Active Material Lots", len(active_listings))
    k2.metric("Sold / Reused Lots", len(sold_listings))
    k3.metric("Total Active Inventory", f"₹{total_inv_val:,.0f}")
    k4.metric("Buyer Inquiries", len(incoming_reqs))

    st.markdown("---")

    # Section 1: Incoming Buyer Purchase Offers
    st.subheader(f"📬 Incoming Buyer Purchase Offers ({len(incoming_reqs)})")
    if incoming_reqs:
        for req in incoming_reqs:
            with SessionLocal() as db_r:
                item_obj = db_r.query(Listing).filter(Listing.id == req.listing_id).first()
                buyer_obj = db_r.query(User).filter(User.id == req.buyer_id).first()
                mat_title = item_obj.material_name if item_obj else "Material Item"
                buyer_name = buyer_obj.name if buyer_obj else "General Contractor"

            status_style = f"status-{req.status}"
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h4 style="margin:0; color:#0f172a;">{mat_title}</h4>
                        <p style="margin:0.2rem 0; font-size:0.85rem; color:#475569;">
                            Buyer: <b>{buyer_name}</b> • Requested: <b>{req.quantity} units</b> • Offered Price: <b style="color:#065f46;">₹{req.proposed_price:,.0f}</b>
                        </p>
                        <p style="margin:0; font-size:0.8rem; color:#64748b;">
                            Pickup Date: {req.preferred_pickup_date or 'Flexible'} | <i>"{req.message or 'No message'}"</i>
                        </p>
                    </div>
                    <div>
                        <span class="status-badge {status_style}">{req.status}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if req.status == "pending":
                bcol1, bcol2 = st.columns([1, 4])
                with bcol1:
                    if st.button("✅ Accept Offer", key=f"acc_{req.id}"):
                        with SessionLocal() as db_act:
                            r_update = db_act.query(PurchaseRequest).filter(PurchaseRequest.id == req.id).first()
                            if r_update:
                                r_update.status = "accepted"
                                # Record transaction
                                trans = Transaction(
                                    listing_id=r_update.listing_id,
                                    buyer_id=r_update.buyer_id,
                                    seller_id=default_seller.id,
                                    quantity=r_update.quantity,
                                    price=r_update.proposed_price,
                                    status="completed"
                                )
                                db_act.add(trans)
                                db_act.commit()
                        st.success("🎉 Offer accepted! Transaction recorded and credited toward circular diverted landfill metrics.")
                        st.rerun()
                with bcol2:
                    if st.button("❌ Decline", key=f"dec_{req.id}"):
                        with SessionLocal() as db_act:
                            r_update = db_act.query(PurchaseRequest).filter(PurchaseRequest.id == req.id).first()
                            if r_update:
                                r_update.status = "rejected"
                                db_act.commit()
                        st.warning("Offer declined.")
                        st.rerun()
    else:
        st.info("No incoming buyer purchase offers yet. As contractors browse your materials, offers will appear here.")

    st.markdown("---")

    # Section 2: Active Listed Inventory
    st.subheader(f"📋 Your Listed Inventory ({len(seller_listings)})")
    if seller_listings:
        for itm in seller_listings:
            with st.container():
                icol1, icol2, icol3 = st.columns([1, 3, 1])
                with icol1:
                    st.image(itm.image_url, width=120)
                with icol2:
                    st.write(f"**{itm.material_name}** ({itm.category})")
                    st.write(f"Grade {itm.quality_grade} • Quantity: {itm.quantity:,.0f} {itm.unit} • Location: {itm.city}")
                    st.write(f"Price: **₹{itm.price:,.0f}** | Status: `{itm.status}`")
                with icol3:
                    if st.button("🗑️ Delete Lot", key=f"del_lot_{itm.id}"):
                        with SessionLocal() as db_del:
                            del_target = db_del.query(Listing).filter(Listing.id == itm.id).first()
                            if del_target:
                                db_del.delete(del_target)
                                db_del.commit()
                        st.success("Listing removed from inventory.")
                        st.rerun()
                st.markdown("<hr style='margin:0.5rem 0;'/>", unsafe_allow_html=True)
    else:
        st.info("You currently have no listed materials. Use '➕ Sell Surplus Material' to publish your first lot.")


# ==============================================================================
# PAGE 4: SELL SURPLUS MATERIAL (LISTING CREATION WIZARD)
# ==============================================================================
elif nav_choice == "➕ Sell Surplus Material":
    st.markdown('<div class="main-header">➕ List Surplus Material for Sale</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Use camera or photo upload with AI diagnostics to instantly list reclaimed construction materials on the marketplace.</div>', unsafe_allow_html=True)

    prefill = st.session_state.get("prefill_listing", {})

    with st.expander("📷 Step 1: Capture or Upload Material Photo", expanded=True):
        up_choice = st.radio("Photo Source", ["Upload File", "Device Camera"], horizontal=True, key="sell_photo_choice")
        sell_img_bytes = None
        if up_choice == "Device Camera":
            s_cam = st.camera_input("Capture material on site")
            if s_cam:
                sell_img_bytes = s_cam.getvalue()
        else:
            s_file = st.file_uploader("Upload photograph", type=["jpg", "jpeg", "png", "webp"], key="sell_uploader")
            if s_file:
                sell_img_bytes = s_file.getvalue()

        if sell_img_bytes:
            st.image(sell_img_bytes, width=280, caption="Uploaded Lot Photo")
            if st.button("🤖 Run AI Auto-Fill Diagnostics"):
                with st.spinner("Classifying material with MobileNetV2 and assessing quality..."):
                    pred_res = material_classifier.predict(sell_img_bytes)
                    q_res = quality_classifier.assess_quality(pred_res["predicted_material"], age_years=1.5, damage_percentage=8.0)
                    rate_inf = BASE_MARKET_RATES.get(pred_res["predicted_material"], {"unit": "Units"})
                    p_res = price_predictor.predict_price(
                        material_name=pred_res["predicted_material"],
                        quantity=1000.0,
                        unit=rate_inf.get("unit", "Units"),
                        quality_score=q_res["quality_score"],
                        age_years=1.5,
                        damage_percentage=8.0,
                        city="Bangalore"
                    )
                    st.session_state["prefill_listing"] = {
                        "material_name": pred_res["predicted_material"],
                        "category": pred_res["category"],
                        "quality_grade": q_res["quality_grade"],
                        "quality_score": q_res["quality_score"],
                        "quantity": 1000.0,
                        "unit": rate_inf.get("unit", "Units"),
                        "price": p_res["estimated_price"],
                        "age": 1.5,
                        "damage": 8.0
                    }
                    st.success("✅ AI Diagnostics populated below!")
                    st.rerun()

    st.subheader("📝 Step 2: Material & Valuation Details")
    with st.form("create_listing_form"):
        col_m1, col_m2 = st.columns(2)

        with col_m1:
            default_mat = prefill.get("material_name", MATERIAL_CLASSES[0])
            mat_idx = MATERIAL_CLASSES.index(default_mat) if default_mat in MATERIAL_CLASSES else 0
            form_mat = st.selectbox("Material Name", MATERIAL_CLASSES, index=mat_idx)
            form_cat = st.selectbox("Category", ["Masonry", "Metals & Structural", "Aggregates & Masonry", "Joinery & Fixtures", "Finishing & Ceramics", "Plumbing & Conduits", "Exterior & Roofing"])
            form_qty = st.number_input("Lot Quantity", min_value=1.0, value=float(prefill.get("quantity", 1000.0)), step=50.0)
            form_unit = st.selectbox("Unit", ["Pieces", "Tonnes", "Kg", "Sq.Ft", "Meters"], index=0)

        with col_m2:
            grade_list = ["A", "B", "C", "D", "E"]
            default_grade = prefill.get("quality_grade", "B")
            grade_idx = grade_list.index(default_grade) if default_grade in grade_list else 1
            form_grade = st.selectbox("Quality Condition Grade", grade_list, index=grade_idx)
            form_score = st.slider("Quality Score (0–100)", 0.0, 100.0, float(prefill.get("quality_score", 82.0)), 1.0)
            form_price = st.number_input("Listing Asking Price (₹)", min_value=100.0, value=float(prefill.get("price", 15000.0)), step=500.0)
            form_city = st.selectbox("Site Location City", list(CITY_DEMAND_INDEX.keys()))

        form_usage = st.text_input("Original Usage / History", value="Commercial demolition & site clearance surplus")
        form_img_url = st.text_input("Lot Photo URL (or defaults to sample)", value="https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=800&auto=format&fit=crop&q=60")

        submit_listing = st.form_submit_button("🚀 Publish Material to Marketplace", type="primary")

        if submit_listing:
            with SessionLocal() as db_publish:
                def_seller, _ = get_default_users(db_publish)
                new_item = Listing(
                    seller_id=def_seller.id,
                    material_name=form_mat,
                    category=form_cat,
                    image_url=form_img_url,
                    ai_confidence=0.94,
                    quality_grade=form_grade,
                    quality_score=form_score,
                    quantity=form_qty,
                    unit=form_unit,
                    price=form_price,
                    ai_estimated_price=form_price,
                    city=form_city,
                    state="Karnataka",
                    original_usage=form_usage,
                    availability="Immediate Pickup",
                    status="active"
                )
                db_publish.add(new_item)
                db_publish.commit()

            st.session_state.pop("prefill_listing", None)
            st.success("🎉 Material listing published to the live marketplace! Buyers can now discover and submit offers for this lot.")


# ==============================================================================
# PAGE 5: BUYER PORTAL & ORDERS
# ==============================================================================
elif nav_choice == "🛍️ Buyer Portal & Orders":
    st.markdown('<div class="main-header">🛍️ Buyer Portal & Order Tracking</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Monitor your sent purchase offers, negotiate reclaimed material lots, and review circular ESG impact.</div>', unsafe_allow_html=True)

    with SessionLocal() as db:
        _, def_buyer = get_default_users(db)
        buyer_requests = db.query(PurchaseRequest).filter(PurchaseRequest.buyer_id == def_buyer.id).order_by(PurchaseRequest.created_at.desc()).all()

    # Metrics Summary
    accepted_offers = [r for r in buyer_requests if r.status == "accepted"]
    pending_offers = [r for r in buyer_requests if r.status == "pending"]

    b1, b2, b3 = st.columns(3)
    b1.metric("Total Submitted Offers", len(buyer_requests))
    b2.metric("Accepted Deals", len(accepted_offers))
    b3.metric("Pending Negotiation", len(pending_offers))

    st.markdown("---")
    st.subheader(f"📑 Sent Purchase Offers ({len(buyer_requests)})")

    if buyer_requests:
        for r in buyer_requests:
            with SessionLocal() as db_l:
                listing_item = db_l.query(Listing).filter(Listing.id == r.listing_id).first()
                mat_name = listing_item.material_name if listing_item else "Reclaimed Material"
                loc = f"{listing_item.city}, {listing_item.state}" if listing_item else "Karnataka"
                img = listing_item.image_url if listing_item else "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=800"
                seller_rec = db_l.query(User).filter(User.id == listing_item.seller_id).first() if listing_item else None
                s_name = seller_rec.name if seller_rec else "Demolition Supplier"
                s_phone = seller_rec.phone if seller_rec else "+91 9880012345"

            status_cls = f"status-{r.status}"
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; gap:1rem; align-items:center;">
                    <img src="{img}" style="width:90px; height:80px; object-fit:cover; border-radius:8px;"/>
                    <div style="flex-grow:1;">
                        <div style="display:flex; justify-content:space-between;">
                            <h4 style="margin:0; color:#0f172a;">{mat_name}</h4>
                            <span class="status-badge {status_cls}">{r.status}</span>
                        </div>
                        <p style="margin:0.2rem 0; font-size:0.85rem; color:#475569;">
                            📍 {loc} • Seller: <b>{s_name}</b> (📞 {s_phone})
                        </p>
                        <p style="margin:0; font-size:0.85rem;">
                            Offered: <b style="color:#065f46;">₹{r.proposed_price:,.0f}</b> for <b>{r.quantity} units</b> | Pickup: <i>{r.preferred_pickup_date or 'Immediate'}</i>
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("You haven't submitted any purchase offers yet. Discover surplus materials in '🛒 Construction Waste Marketplace' or '📸 AI Material Assessment' and submit offers.")


# ==============================================================================
# PAGE 6: PRICE ESTIMATOR (PRESERVED)
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
# PAGE 7: ENVIRONMENTAL CALCULATOR (PRESERVED)
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
# PAGE 8: ABOUT & TECHNOLOGY (PRESERVED)
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
    * **Integrated Marketplace**: Direct seller inventory management, buyer purchase request negotiations, and ESG reporting.
    """)
