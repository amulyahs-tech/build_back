# REBUILD AI — System Architecture & Methodology

## 1. Overview
REBUILD AI is an end-to-end full-stack artificial intelligence and circular economy platform engineered to transform construction and demolition (C&D) waste management. It connects demolition contractors, builders, recyclers, and architects to evaluate, price, list, and trade salvaged materials with high trust.

## 2. Core Architectural Components

### A. Computer Vision Material Classifier
* **Base Architecture**: MobileNetV2 with depthwise separable convolutions pre-trained on ImageNet.
* **Input**: 224×224×3 RGB tensor with standard channel normalization.
* **Feature Embeddings**: 1,280-dimensional normalized unit vector generated from the global average pooling layer.
* **Material Classes (20)**:
  1. Bricks
  2. Concrete
  3. Cement Blocks
  4. Steel / Rebar
  5. Wood / Timber
  6. Tiles
  7. Glass
  8. PVC Pipes
  9. Metal Pipes
  10. Doors
  11. Windows
  12. Electrical Components
  13. Roofing Materials
  14. Stones
  15. Sand
  16. Marble
  17. Granite
  18. Ceramic Materials
  19. Mixed Construction Waste
  20. Other / Debris
* **Low Confidence Alert**: Flags images with top probability < 0.70 to prompt clearer site lighting or manual confirmation.

### B. Multimodal Quality Assessment Engine
* Evaluates material condition into **Grades A, B, C, D, E** mapped to a numerical **0–100 condition score**:
  * **Grade A (92–100)**: Excellent, negligible micro-wear. Certified for direct structural reuse.
  * **Grade B (80–91)**: Good, minor surface weathering. Suitable for secondary walls and non-critical framing.
  * **Grade C (65–79)**: Moderate, noticeable wear or mortar residue. Recommended for non-load-bearing partitions, landscaping, or pavers.
  * **Grade D (40–64)**: Poor, substantial fragmentation. Reusable after mechanical processing (e.g. crushing into road-base aggregates).
  * **Grade E (0–39)**: Very Poor, contaminated/heavy fractures. Downcycling or inert daily landfill cover only.
* Integrates visual texture indicators with user metadata: age in years, percentage wear, and original structural context.

### C. Valuation Engine (Gradient Boosting Regressor)
* **Production Model**: Gradient Boosting Regressor ($R^2 \approx 0.935–0.951$, MAE $\approx$ ₹3,546).
* **Feature Vector**: `[material_type, city, quality_score, age_years, damage_percentage, quantity]`.
* **Outputs**: Fair second-hand market price (INR), negotiation range (min–max $\pm 12\%$), unit rate, and percentage discount versus brand-new virgin material.

### D. Visual Similarity Engine
* Computes cosine distance across active listings' 1280-dimensional MobileNetV2 embeddings:
  $$\text{Similarity}(A, B) = \frac{A \cdot B}{\|A\|_2 \|B\|_2} \times 100\%$$
* Allows contractors to photograph an unknown salvage element on-site and retrieve visually and materially matching inventory across the network.

### E. Circular Life Cycle Assessment (LCA) Calculator
* Quantifies environmental benefits based on construction embodied carbon metrics (ICE Bath Inventory & Environmental Product Declarations):
  * **Landfill Mass Diverted**: $\text{Quantity} \times \text{Density Factor (tonnes)}$
  * **Avoided Embodied Carbon**: $\text{Mass (kg)} \times \text{Virgin Embodied Carbon Factor (kg CO}_2\text{e/kg)}$
  * **Virgin Extraction Preserved**: Tonnes of limestone, bauxite, iron ore, or timber preserved.
  * **Tree Sequestration Equivalence**: Avoided $\text{CO}_2\text{e} / 22 \text{ kg/year}$.
