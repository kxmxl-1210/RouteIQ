"""
RouteIQ - Route Optimizer
Uses Nearest Neighbor heuristic + distance matrix to optimize delivery routes
"""

import numpy as np
import random


# Sample Indian city coordinates
CITY_COORDS = {
    'Chennai':     (13.0827, 80.2707),
    'Mumbai':      (19.0760, 72.8777),
    'Delhi':       (28.6139, 77.2090),
    'Bangalore':   (12.9716, 77.5946),
    'Hyderabad':   (17.3850, 78.4867),
    'Kolkata':     (22.5726, 88.3639),
    'Pune':        (18.5204, 73.8567),
    'Ahmedabad':   (23.0225, 72.5714),
    'Coimbatore':  (11.0168, 76.9558),
    'Madurai':     (9.9252,  78.1198),
    'Jaipur':      (26.9124, 75.7873),
    'Surat':       (21.1702, 72.8311),
    'Lucknow':     (26.8467, 80.9462),
    'Nagpur':      (21.1458, 79.0882),
    'Visakhapatnam': (17.6868, 83.2185),
}


def haversine(coord1, coord2):
    """Calculate distance in km between two lat/lon coords."""
    R = 6371
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))


def nearest_neighbor_route(cities, start=None):
    """
    Greedy nearest-neighbor TSP heuristic.
    Returns optimized order of cities.
    """
    if len(cities) <= 1:
        return cities, 0

    unvisited = cities.copy()
    if start and start in unvisited:
        current = start
        unvisited.remove(start)
    else:
        current = unvisited.pop(0)

    route = [current]
    total_distance = 0

    while unvisited:
        coords_current = CITY_COORDS.get(current, (0, 0))
        nearest = min(unvisited,
                      key=lambda c: haversine(coords_current, CITY_COORDS.get(c, (0, 0))))
        dist = haversine(coords_current, CITY_COORDS.get(nearest, (0, 0)))
        total_distance += dist
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return route, round(total_distance, 2)


def original_route_distance(cities):
    """Calculate total distance of original (unoptimized) route."""
    total = 0
    for i in range(len(cities) - 1):
        c1 = CITY_COORDS.get(cities[i], (0, 0))
        c2 = CITY_COORDS.get(cities[i+1], (0, 0))
        total += haversine(c1, c2)
    return round(total, 2)


def get_route_coordinates(cities):
    """Return list of (lat, lon) for a list of cities."""
    return [CITY_COORDS.get(c, (20.5937, 78.9629)) for c in cities]


def optimize_and_compare(cities, start=None):
    """
    Returns a dict with original vs optimized route comparison.
    """
    original_dist = original_route_distance(cities)
    optimized_route, optimized_dist = nearest_neighbor_route(cities, start)
    savings = original_dist - optimized_dist
    savings_pct = (savings / original_dist * 100) if original_dist > 0 else 0

    return {
        'original_route': cities,
        'optimized_route': optimized_route,
        'original_distance_km': original_dist,
        'optimized_distance_km': optimized_dist,
        'savings_km': round(savings, 2),
        'savings_pct': round(savings_pct, 1),
        'estimated_fuel_saved_l': round(savings * 0.12, 2),  # ~12L per 100km
        'estimated_cost_saved_inr': round(savings * 12 * 101, 2),  # ~₹101/L diesel
    }


if __name__ == "__main__":
    sample_cities = ['Chennai', 'Madurai', 'Coimbatore', 'Bangalore', 'Hyderabad', 'Pune']
    result = optimize_and_compare(sample_cities, start='Chennai')
    print("📍 Original Route:", " → ".join(result['original_route']))
    print("🚀 Optimized Route:", " → ".join(result['optimized_route']))
    print(f"📏 Distance Saved: {result['savings_km']} km ({result['savings_pct']}%)")
    print(f"⛽ Fuel Saved: {result['estimated_fuel_saved_l']} L")
    print(f"💰 Cost Saved: ₹{result['estimated_cost_saved_inr']}")
