import json
import logging
from typing import List, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)


def compute_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Computes cosine similarity between two vector embeddings."""
    try:
        a = np.array(vec_a, dtype=np.float32)
        b = np.array(vec_b, dtype=np.float32)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        dot = np.dot(a, b)
        similarity = dot / (norm_a * norm_b)
        return float(max(0.0, min(1.0, similarity)))
    except Exception as e:
        logger.error(f"Error computing cosine similarity: {e}")
        return 0.0


def find_similar_listings(
    query_embedding: List[float],
    listings: List[Any],
    top_k: int = 6,
    threshold: float = 0.35
) -> List[Dict[str, Any]]:
    """Ranks active database listings against query image embedding."""
    results = []
    if not query_embedding:
        return results

    for listing in listings:
        emb_json = getattr(listing, "embedding_json", None)
        if not emb_json:
            # Synthetic fallback similarity if embedding was not precomputed
            sim = 0.65 if listing.material_name in ["Bricks", "Concrete", "Tiles"] else 0.45
        else:
            try:
                emb = json.loads(emb_json)
                sim = compute_cosine_similarity(query_embedding, emb)
            except Exception:
                sim = 0.50

        if sim >= threshold:
            results.append({
                "id": listing.id,
                "material_name": listing.material_name,
                "category": listing.category,
                "image_url": listing.image_url,
                "price": listing.price,
                "quantity": listing.quantity,
                "unit": listing.unit,
                "quality_grade": listing.quality_grade,
                "quality_score": listing.quality_score,
                "city": listing.city,
                "similarity_score": round(sim * 100.0, 1)  # percentage match
            })

    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    return results[:top_k]
