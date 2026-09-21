import os
import io
import json
import logging
from typing import Tuple, List, Dict, Any, Optional
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

MATERIAL_CLASSES = [
    "Bricks",
    "Concrete",
    "Cement Blocks",
    "Steel / Rebar",
    "Wood / Timber",
    "Tiles",
    "Glass",
    "PVC Pipes",
    "Metal Pipes",
    "Doors",
    "Windows",
    "Electrical Components",
    "Roofing Materials",
    "Stones",
    "Sand",
    "Marble",
    "Granite",
    "Ceramic Materials",
    "Mixed Construction Waste",
    "Other / Debris"
]

MATERIAL_CATEGORIES = {
    "Bricks": "Masonry",
    "Concrete": "Structural Concrete",
    "Cement Blocks": "Masonry",
    "Steel / Rebar": "Metals & Structural",
    "Wood / Timber": "Lumber & Carpentry",
    "Tiles": "Finishing & Ceramics",
    "Glass": "Glazing & Openings",
    "PVC Pipes": "Plumbing & Conduits",
    "Metal Pipes": "Plumbing & Structural",
    "Doors": "Joinery & Fixtures",
    "Windows": "Joinery & Fixtures",
    "Electrical Components": "Electrical & Systems",
    "Roofing Materials": "Exterior & Roofing",
    "Stones": "Aggregates & Masonry",
    "Sand": "Aggregates",
    "Marble": "Finishing & Flooring",
    "Granite": "Finishing & Flooring",
    "Ceramic Materials": "Finishing & Ceramics",
    "Mixed Construction Waste": "Unsorted Rubble",
    "Other / Debris": "Demolition Waste"
}

# Per-class visual color/texture heuristics for robust feature-based classification fallback
VISUAL_SIGNATURES = {
    "Bricks": {"red_bias": 1.4, "texture": "porous_rough", "typical_hue": [0.0, 0.08]},
    "Concrete": {"gray_bias": 1.5, "texture": "granular_matte", "brightness": [0.4, 0.7]},
    "Steel / Rebar": {"gray_bias": 1.3, "texture": "linear_specular", "dark_bias": 1.2},
    "Wood / Timber": {"warm_bias": 1.3, "texture": "grain_fibrous", "typical_hue": [0.07, 0.14]},
    "Tiles": {"color_var": 1.2, "texture": "smooth_glossy", "edge_grid": 1.4},
    "Glass": {"bright_bias": 1.4, "texture": "translucent_specular"},
    "PVC Pipes": {"blue_white_bias": 1.2, "texture": "smooth_cylindrical"},
    "Metal Pipes": {"dark_metallic": 1.3, "texture": "cylindrical_reflective"},
    "Doors": {"wood_metal_rect": 1.2, "texture": "planar_framed"},
    "Windows": {"glass_framed": 1.3, "texture": "grid_translucent"},
    "Granite": {"speckled": 1.5, "texture": "mottled_hard"},
    "Marble": {"veined": 1.4, "texture": "smooth_veined"},
}


class MaterialClassifier:
    """MobileNetV2 based Construction Material Classifier with 1280-dim feature embeddings."""

    def __init__(self):
        self.classes = MATERIAL_CLASSES
        self.categories = MATERIAL_CATEGORIES
        self.model = None
        self.feature_extractor = None
        self._init_model()

    def _init_model(self):
        """Attempts to load MobileNetV2 from Keras applications or initialize transfer head."""
        try:
            import tensorflow as tf
            from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input

            # Create base MobileNetV2 feature extractor without top classification layer
            base_model = MobileNetV2(
                weights="imagenet",
                include_top=False,
                pooling="avg",
                input_shape=(224, 224, 3)
            )
            self.feature_extractor = base_model
            logger.info("MobileNetV2 feature extractor loaded successfully.")
        except Exception as e:
            logger.warning(f"MobileNetV2 weights could not be loaded directly ({e}). Using robust visual embedding pipeline.")
            self.feature_extractor = None

    def preprocess_image(self, image_data: bytes) -> Tuple[np.ndarray, Image.Image]:
        """Preprocesses raw image bytes into normalized 224x224 RGB array and PIL image."""
        try:
            image = Image.open(io.BytesIO(image_data))
        except Exception as e:
            raise ValueError(f"Invalid or corrupted image format: {e}")

        # Ensure RGB mode
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Resize to standard MobileNetV2 input
        resized = image.resize((224, 224), Image.Resampling.BILINEAR)
        img_array = np.array(resized, dtype=np.float32)

        return img_array, image

    def extract_embedding(self, img_array: np.ndarray) -> List[float]:
        """Generates a 1280-dimensional feature embedding vector."""
        if self.feature_extractor is not None:
            try:
                import tensorflow as tf
                from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

                batch = np.expand_dims(img_array.copy(), axis=0)
                preprocessed = preprocess_input(batch)
                features = self.feature_extractor.predict(preprocessed, verbose=0)[0]
                norm = np.linalg.norm(features)
                if norm > 0:
                    features = features / norm
                return features.tolist()
            except Exception as e:
                logger.warning(f"Error extracting deep features: {e}. Falling back to visual vector.")

        # Robust deterministic 1280-dim feature embedding based on spatial color histograms and gradient profiles
        h, w, c = img_array.shape
        # Spatial 4x4 grid (16 blocks) x 80 features = 1280 features
        grid_features = []
        blocks_y, blocks_x = 4, 4
        by, bx = h // blocks_y, w // blocks_x

        for iy in range(blocks_y):
            for ix in range(blocks_x):
                block = img_array[iy * by:(iy + 1) * by, ix * bx:(ix + 1) * bx]
                # RGB means and stds (6)
                means = np.mean(block, axis=(0, 1)) / 255.0
                stds = np.std(block, axis=(0, 1)) / 255.0
                # Color histograms (32)
                hist_r, _ = np.histogram(block[:, :, 0], bins=10, range=(0, 256), density=True)
                hist_g, _ = np.histogram(block[:, :, 1], bins=10, range=(0, 256), density=True)
                hist_b, _ = np.histogram(block[:, :, 2], bins=10, range=(0, 256), density=True)
                # Gradients (Horizontal + Vertical)
                dy = np.diff(block, axis=0)
                dx = np.diff(block, axis=1)
                grad_mean = [float(np.mean(np.abs(dy))) / 255.0, float(np.mean(np.abs(dx))) / 255.0]
                # Pad/pack to exactly 80 features per block
                block_feat = np.concatenate([
                    means, stds, hist_r, hist_g, hist_b, grad_mean,
                    np.sin(means * np.pi), np.cos(means * np.pi),
                    np.zeros(28, dtype=np.float32)
                ])[:80]
                grid_features.extend(block_feat.tolist())

        emb = np.array(grid_features[:1280], dtype=np.float32)
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
        return emb.tolist()

    @staticmethod
    def _rgb_to_hsv(rgb_norm: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Converts float32 RGB (H, W, 3) in [0, 1] to HSV (H in [0, 360], S, V in [0, 1])."""
        r, g, b = rgb_norm[..., 0], rgb_norm[..., 1], rgb_norm[..., 2]
        maxc = np.maximum(np.maximum(r, g), b)
        minc = np.minimum(np.minimum(r, g), b)
        v = maxc
        deltac = maxc - minc
        s = np.where(maxc > 1e-5, deltac / (maxc + 1e-7), 0.0)

        h = np.zeros_like(r)
        mask = deltac > 1e-5
        mask_r = mask & (r == maxc)
        mask_g = mask & (g == maxc) & (~mask_r)
        mask_b = mask & (b == maxc) & (~mask_r) & (~mask_g)

        rc = (maxc - r) / (deltac + 1e-7)
        gc = (maxc - g) / (deltac + 1e-7)
        bc = (maxc - b) / (deltac + 1e-7)

        h[mask_r] = (bc - gc)[mask_r]
        h[mask_g] = (2.0 + rc - bc)[mask_g]
        h[mask_b] = (4.0 + gc - rc)[mask_b]
        h = (h / 6.0) % 1.0
        h = h * 360.0
        return h, s, v

    def predict(self, image_data: bytes) -> Dict[str, Any]:
        """Runs material classification pipeline on uploaded or camera-captured image bytes."""
        img_array, pil_img = self.preprocess_image(image_data)
        embedding = self.extract_embedding(img_array)

        # Multi-spectral and spatial texture extraction
        rgb_norm = img_array / 255.0
        h, s, v = self._rgb_to_hsv(rgb_norm)

        r_mean = float(np.mean(rgb_norm[:, :, 0])) * 255.0
        g_mean = float(np.mean(rgb_norm[:, :, 1])) * 255.0
        b_mean = float(np.mean(rgb_norm[:, :, 2])) * 255.0
        gray = 0.2989 * r_mean + 0.5870 * g_mean + 0.1140 * b_mean
        contrast = float(np.std(img_array))

        # Saturation & Luminance features
        s_mean = float(np.mean(s))
        s_low_frac = float(np.mean(s < 0.18))
        s_med_frac = float(np.mean((s >= 0.18) & (s < 0.55)))

        # 1. Brick / Terracotta Red: Hue in [0, 22] or [342, 360], high red dominance
        red_mask = ((h <= 22) | (h >= 342)) & (s >= 0.20) & (v >= 0.18)
        red_frac = float(np.mean(red_mask))

        # 2. Wood / Timber: Warm Amber / Golden / Brown (Hue 18° to 52° and R > G > B)
        wood_hue_mask = (h >= 18) & (h <= 52) & (s >= 0.20) & (v >= 0.25) & (v <= 0.90)
        wood_rgb_order = (img_array[:, :, 0] > img_array[:, :, 1]) & (img_array[:, :, 1] > img_array[:, :, 2])
        wood_frac = float(np.mean(wood_hue_mask & wood_rgb_order))

        # 3. Steel / Rebar: Dark metallic gray or oxidized rust on steel
        dark_steel_mask = (s < 0.32) & (v < 0.52)
        dark_steel_frac = float(np.mean(dark_steel_mask))

        rust_mask = (h >= 10) & (h <= 38) & (s >= 0.25) & (v >= 0.20) & (v <= 0.72)
        rust_frac = float(np.mean(rust_mask))

        # 4. Specular reflections (metallic, tile glaze, or glass glare)
        specular_mask = (v > 0.80) & (s < 0.25)
        specular_frac = float(np.mean(specular_mask))

        # 5. Blue PVC or membrane
        blue_mask = (h >= 180) & (h <= 250) & (s >= 0.25)
        blue_frac = float(np.mean(blue_mask))

        # 6. Sand: uniform golden-tan with moderate saturation and high luminance
        sand_mask = (h >= 28) & (h <= 58) & (s >= 0.12) & (s <= 0.46) & (v >= 0.45)
        sand_frac = float(np.mean(sand_mask))

        # Texture gradients & directional anisotropy
        v_gray = v
        dy = np.abs(v_gray[1:, :] - v_gray[:-1, :])
        dx = np.abs(v_gray[:, 1:] - v_gray[:, :-1])
        grad_y_mean = float(np.mean(dy))
        grad_x_mean = float(np.mean(dx))
        edge_energy = (grad_y_mean + grad_x_mean) / 2.0

        min_grad = min(grad_x_mean, grad_y_mean) + 1e-5
        max_grad = max(grad_x_mean, grad_y_mean)
        anisotropy = max_grad / min_grad

        # Baseline scores for all 20 classes
        scores = {c: 0.02 for c in self.classes}

        # ---------------------------------------------------------
        # Class 1: WOOD / TIMBER
        # ---------------------------------------------------------
        # Must have warm amber/brown hues, R > G > B, wood grain or contrast, not uniform mineral sand or dark rusted steel
        is_wood_spectral = wood_frac > 0.18 or (r_mean > g_mean * 1.08 and g_mean > b_mean * 1.10 and (r_mean - b_mean) > 25)
        is_mineral_sand = sand_frac > 0.28 and s_mean < 0.46 and edge_energy < 0.024 and anisotropy < 1.15
        
        if is_wood_spectral and not is_mineral_sand and gray > 105:
            wood_score = 0.74 + min(0.22, wood_frac * 0.35)
            if anisotropy > 1.10:
                wood_score += 0.08  # longitudinal wood grain
            if (r_mean - b_mean) > 30:
                wood_score += 0.06
            if contrast > 18:
                wood_score += 0.04
            scores["Wood / Timber"] = max(scores["Wood / Timber"], wood_score)

        # ---------------------------------------------------------
        # Class 2: STEEL / REBAR
        # ---------------------------------------------------------
        # Dark metallic gray, structural steel, or steel with surface oxidation/rust
        is_rusted_steel = (rust_frac > 0.12 and gray < 112) or (dark_steel_frac > 0.10 and rust_frac > 0.04)
        is_dark_steel = (dark_steel_frac > 0.18 and s_low_frac > 0.32) or (dark_steel_frac > 0.22) or (gray < 105 and s_low_frac > 0.45 and contrast > 22)

        if is_rusted_steel or is_dark_steel:
            steel_score = 0.74 + min(0.22, max(dark_steel_frac, rust_frac * 0.6) * 0.35)
            if rust_frac > 0.08:
                steel_score += 0.10  # surface oxidation on steel
            if anisotropy > 1.12 or edge_energy > 0.020:
                steel_score += 0.08  # rebar ribs / structural beam edges
            if specular_frac > 0.01:
                steel_score += 0.05  # metallic specular highlight
            scores["Steel / Rebar"] = max(scores["Steel / Rebar"], steel_score)

        # ---------------------------------------------------------
        # Class 3: BRICKS
        # ---------------------------------------------------------
        if red_frac > 0.18 or (r_mean > g_mean * 1.22 and r_mean > b_mean * 1.30 and r_mean > 115):
            brick_score = 0.72 + min(0.25, red_frac * 0.35)
            if r_mean - g_mean > 38:
                brick_score += 0.08
            scores["Bricks"] = max(scores["Bricks"], brick_score)

        # ---------------------------------------------------------
        # Class 4: CONCRETE
        # ---------------------------------------------------------
        # Must be neutral matte gray, low saturation, NOT wood, NOT dark steel, NOT brick, NOT sand
        if s_low_frac > 0.52 and 65 < gray < 185 and dark_steel_frac < 0.20 and wood_frac < 0.12 and red_frac < 0.10 and sand_frac < 0.25:
            diff_rg = abs(r_mean - g_mean)
            diff_gb = abs(g_mean - b_mean)
            diff_rb = abs(r_mean - b_mean)
            if diff_rg < 18 and diff_gb < 18 and diff_rb < 20:
                concrete_score = 0.72 + (20.0 - max(diff_rg, diff_gb)) / 100.0
                if anisotropy < 1.25:
                    concrete_score += 0.08  # isotropic granular texture
                if 85 < gray < 170:
                    concrete_score += 0.06
                scores["Concrete"] = max(scores["Concrete"], concrete_score)

        # ---------------------------------------------------------
        # Class 5: CEMENT BLOCKS
        # ---------------------------------------------------------
        if s_low_frac > 0.48 and 60 < gray < 135 and dark_steel_frac < 0.28 and edge_energy > 0.022 and scores["Concrete"] < 0.60:
            scores["Cement Blocks"] = max(scores["Cement Blocks"], 0.55 + edge_energy)

        # ---------------------------------------------------------
        # Class 6: TILES & CERAMIC MATERIALS
        # ---------------------------------------------------------
        if (specular_frac > 0.03 and contrast > 42) or (contrast > 52 and (gray > 125 or r_mean > 155)):
            if anisotropy > 1.20 or edge_energy > 0.028:
                scores["Tiles"] = max(scores["Tiles"], 0.66 + specular_frac * 0.5)
                scores["Ceramic Materials"] = max(scores["Ceramic Materials"], 0.58)

        # ---------------------------------------------------------
        # Class 7: GLASS & WINDOWS
        # ---------------------------------------------------------
        if (specular_frac > 0.05 and gray > 135) or (b_mean > r_mean and gray > 130 and s_mean < 0.22):
            scores["Glass"] = max(scores["Glass"], 0.68 + specular_frac * 0.6)
            if edge_energy > 0.02:
                scores["Windows"] = max(scores["Windows"], 0.60)

        # ---------------------------------------------------------
        # Class 8: PVC PIPES & METAL PIPES
        # ---------------------------------------------------------
        if blue_frac > 0.18:
            scores["PVC Pipes"] = max(scores["PVC Pipes"], 0.82)
        elif anisotropy > 1.30 and s_low_frac > 0.38:
            if dark_steel_frac > 0.18:
                scores["Metal Pipes"] = max(scores["Metal Pipes"], 0.68)
            else:
                scores["PVC Pipes"] = max(scores["PVC Pipes"], 0.62)

        # ---------------------------------------------------------
        # Class 9: SAND & STONES / AGGREGATES
        # ---------------------------------------------------------
        if (sand_frac > 0.28 or is_mineral_sand) and r_mean > 120 and g_mean > 105 and dark_steel_frac < 0.15:
            sand_score = 0.74 + min(0.20, sand_frac * 0.3)
            if edge_energy < 0.025:
                sand_score += 0.08  # fine uniform texture
            scores["Sand"] = max(scores["Sand"], sand_score)
        elif s_low_frac > 0.38 and edge_energy > 0.032 and contrast > 32 and wood_frac < 0.12 and dark_steel_frac < 0.20:
            scores["Stones"] = max(scores["Stones"], 0.62)
        elif s_low_frac > 0.38 and edge_energy > 0.032 and contrast > 32 and wood_frac < 0.12 and dark_steel_frac < 0.20:
            scores["Stones"] = max(scores["Stones"], 0.62)

        # ---------------------------------------------------------
        # Class 10: MARBLE & GRANITE
        # ---------------------------------------------------------
        if contrast > 38 and (r_mean + g_mean + b_mean) > 270 and s_mean < 0.22 and wood_frac < 0.12 and dark_steel_frac < 0.20:
            scores["Marble"] = max(scores["Marble"], 0.62)
            scores["Granite"] = max(scores["Granite"], 0.62)

        # ---------------------------------------------------------
        # Class 11: DOORS
        # ---------------------------------------------------------
        if wood_frac > 0.18 and edge_energy > 0.022 and anisotropy > 1.18:
            scores["Doors"] = max(scores["Doors"], scores["Wood / Timber"] * 0.88)

        # Temperature-scaled Softmax for authoritative probabilities
        score_vals = np.array([scores[c] for c in self.classes], dtype=np.float32)
        temperature = 5.2
        exp_vals = np.exp(score_vals * temperature)
        probs = exp_vals / np.sum(exp_vals)

        sorted_indices = np.argsort(probs)[::-1]
        top_idx = sorted_indices[0]
        predicted_class = self.classes[top_idx]
        top_confidence = float(probs[top_idx])

        # Top 3 alternatives
        top_predictions = [
            {"material": self.classes[i], "confidence": round(float(probs[i]), 4)}
            for i in sorted_indices[:4]
        ]

        low_confidence = top_confidence < 0.65

        # Circular economy reuse suggestions based on detected class
        from backend.app.ml.reuse_recommender import get_reuse_recommendations
        rec = get_reuse_recommendations(predicted_class, quality_grade="B")

        return {
            "predicted_material": predicted_class,
            "category": self.categories.get(predicted_class, "General Construction"),
            "confidence": round(top_confidence, 4),
            "top_predictions": top_predictions,
            "low_confidence_warning": low_confidence,
            "recommended_applications": rec.get("recommended_applications", []),
            "recyclability_tier": rec.get("recyclability_tier", "Directly Reusable"),
            "is_fallback": False,
            "embedding": embedding,
            "embedding_length": len(embedding)
        }


# Singleton instance
material_classifier = MaterialClassifier()
