# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Visual Search MCP Server
FastMCP standard interface for perceptual dHash difference and color histogram matching.
"""

import json
from typing import Dict, Any, List
from client import OpenClawGenParkVisualSearch

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("openclaw-genpark-visual-search")
except ImportError:
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(f):
                return f
            return decorator
    mcp = MockFastMCP("openclaw-genpark-visual-search")

vs = OpenClawGenParkVisualSearch()

@mcp.tool()
def compute_perceptual_dhash_from_matrix(
    pixel_matrix_8x9: List[List[int]]
) -> str:
    """
    Computes 64-bit difference hash (dHash) from an 8x9 grayscale pixel matrix.
    """
    res = vs.compute_perceptual_dhash_from_matrix(pixel_matrix_8x9)
    return json.dumps(res, indent=2)

@mcp.tool()
def calculate_hamming_distance_similarity(
    hash_hex_a: str,
    hash_hex_b: str
) -> str:
    """
    Calculates Hamming distance and similarity percentage between two 64-bit hexadecimal hashes.
    """
    res = vs.calculate_hamming_distance_similarity(hash_hex_a, hash_hex_b)
    return json.dumps(res, indent=2)

@mcp.tool()
def compare_color_histograms(
    hist_a_rgb: Dict[str, List[float]],
    hist_b_rgb: Dict[str, List[float]]
) -> str:
    """
    Computes normalized histogram intersection and Euclidean distance across RGB color channels.
    """
    res = vs.compare_color_histograms(hist_a_rgb, hist_b_rgb)
    return json.dumps(res, indent=2)

def main():
    print("Testing Visual Search:")
    print(calculate_hamming_distance_similarity("8f3a09e1b2c45d6f", "8f3a09e1b2c45d6e"))

if __name__ == "__main__":
    main()
