# -*- coding: utf-8 -*-
from client import OpenClawGenParkVisualSearch

vs = OpenClawGenParkVisualSearch()

# Sample 8x9 matrix
matrix = [
    [100, 110, 120, 130, 140, 150, 160, 170, 180],
    [90, 105, 115, 125, 135, 145, 155, 165, 175],
    [80, 95, 105, 115, 125, 135, 145, 155, 165],
    [70, 85, 95, 105, 115, 125, 135, 145, 155],
    [60, 75, 85, 95, 105, 115, 125, 135, 145],
    [50, 65, 75, 85, 95, 105, 115, 125, 135],
    [40, 55, 65, 75, 85, 95, 105, 115, 125],
    [30, 45, 55, 65, 75, 85, 95, 105, 115]
]

# 1. dHash
h1 = vs.compute_perceptual_dhash_from_matrix(matrix)
print(f"Perceptual dHash: {h1['dhash_hex']} (Density: {h1['bit_density_pct']}%)")

# 2. Hamming Distance Match
h2 = "0000000000000003"
match = vs.calculate_hamming_distance_similarity(h1['dhash_hex'], h2)
print()
print(f"Hamming Similarity: {match['similarity_percentage']}% (Dist={match['hamming_distance']}, {match['match_status']})")

# 3. Color Histogram Intersection
hist1 = {"r": [0.4, 0.4, 0.2], "g": [0.3, 0.5, 0.2], "b": [0.2, 0.4, 0.4]}
hist2 = {"r": [0.35, 0.45, 0.2], "g": [0.3, 0.5, 0.2], "b": [0.25, 0.35, 0.4]}
col = vs.compare_color_histograms(hist1, hist2)
print()
print(f"Color Histogram: Intersection={col['histogram_intersection_score']} (Match: {col['color_match_confidence']}%)")
