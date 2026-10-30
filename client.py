# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Visual Search Client
Pure Python Standard Library (Zero External Dependencies)
Implements perceptual difference hashing (dHash), Hamming distance similarity,
and 3D color histogram Euclidean distance matching.
"""

import math
from typing import Dict, Any, List, Optional

class OpenClawGenParkVisualSearch:
    """
    Algorithmic visual comparison and perceptual hashing engine for catalog search agents.
    """

    def __init__(self):
        pass

    def compute_perceptual_dhash_from_matrix(
        self,
        pixel_matrix_8x9: List[List[int]]
    ) -> Dict[str, Any]:
        """
        Computes 64-bit difference hash (dHash) from an 8-row by 9-column grayscale pixel matrix (0-255).
        Each bit is 1 if pixel[r][c] > pixel[r][c+1], else 0.
        """
        if len(pixel_matrix_8x9) < 8 or any(len(row) < 9 for row in pixel_matrix_8x9):
            # Fallback zero-filled 64-bit hash
            return {"dhash_hex": "0" * 16, "bit_length": 64, "active_bits": 0}

        bit_string = ""
        for r in range(8):
            for c in range(8):
                left = pixel_matrix_8x9[r][c]
                right = pixel_matrix_8x9[r][c + 1]
                bit_string += "1" if left > right else "0"

        # Convert 64-bit string to 16 hex characters
        val = int(bit_string, 2)
        hex_hash = f"{val:016x}"
        active_bits = bit_string.count("1")

        return {
            "dhash_hex": hex_hash,
            "bit_length": 64,
            "active_bits": active_bits,
            "bit_density_pct": round((active_bits / 64.0) * 100.0, 2)
        }

    def calculate_hamming_distance_similarity(
        self,
        hash_hex_a: str,
        hash_hex_b: str
    ) -> Dict[str, Any]:
        """
        Calculates Hamming distance between two 64-bit hexadecimal hashes using bitwise XOR:
          distance = popcount(val_a ^ val_b)
          similarity = 1.0 - (distance / 64.0)
        """
        val_a = int(hash_hex_a, 16) if hash_hex_a else 0
        val_b = int(hash_hex_b, 16) if hash_hex_b else 0

        xor_val = val_a ^ val_b
        # Python 3.10+ int.bit_count() is standard library
        distance = xor_val.bit_count() if hasattr(xor_val, "bit_count") else bin(xor_val).count("1")
        
        similarity = round(max(0.0, 1.0 - (distance / 64.0)), 4)

        if distance <= 5:
            match_status = "EXACT_OR_NEAR_IDENTICAL"
        elif distance <= 12:
            match_status = "HIGHLY_SIMILAR_VARIANT"
        elif distance <= 22:
            match_status = "STRUCTURALLY_RELATED"
        else:
            match_status = "DISTINCT_IMAGE"

        return {
            "hash_a": hash_hex_a,
            "hash_b": hash_hex_b,
            "hamming_distance": distance,
            "similarity_percentage": round(similarity * 100.0, 2),
            "match_status": match_status
        }

    def compare_color_histograms(
        self,
        hist_a_rgb: Dict[str, List[float]],
        hist_b_rgb: Dict[str, List[float]]
    ) -> Dict[str, Any]:
        """
        Computes normalized histogram intersection and Euclidean distance across R, G, B color channels.
        """
        intersection_sum = 0.0
        euclidean_sq_sum = 0.0
        total_bins = 0

        for channel in ["r", "g", "b"]:
            bins_a = hist_a_rgb.get(channel, [])
            bins_b = hist_b_rgb.get(channel, [])
            
            num_bins = min(len(bins_a), len(bins_b))
            total_bins += num_bins

            for i in range(num_bins):
                va = max(0.0, float(bins_a[i]))
                vb = max(0.0, float(bins_b[i]))
                
                intersection_sum += min(va, vb)
                euclidean_sq_sum += (va - vb) ** 2

        euclidean_dist = math.sqrt(euclidean_sq_sum)
        # Normalized intersection assuming each channel sums to 1.0 (total 3.0)
        norm_intersection = round(min(1.0, intersection_sum / 3.0), 4) if total_bins > 0 else 0.0

        return {
            "histogram_intersection_score": norm_intersection,
            "euclidean_distance": round(euclidean_dist, 4),
            "color_match_confidence": round(norm_intersection * 100.0, 2)
        }
