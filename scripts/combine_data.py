#!/usr/bin/env python3
"""
Combine parcel geometries with zoning data to create a single source of truth GeoJSON file.

This script merges:
1. Parcel geometries
2. Current height limits
3. Current zoning districts
4. Proposed rezoning (June 2025)
5. Neighborhoods

Output: web-app/public/parcels_combined.geojson
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_PATH = BASE_DIR / "web-app" / "public" / "parcels_combined.geojson"

print("Loading parcel geometries...")
parcels = gpd.read_file(DATA_DIR / "parcels-all.geojson")
print(f"  Loaded {len(parcels)} parcels")

print("\nLoading current height limits...")
heights = gpd.read_file(DATA_DIR / "zoning-height-bulk.geojson")
heights = heights[['gen_hght', 'height', 'geometry']].rename(columns={
    'gen_hght': 'current_height_num',
    'height': 'current_height_code'
})
print(f"  Loaded {len(heights)} height districts")

print("\nLoading current zoning districts...")
zoning = gpd.read_file(DATA_DIR / "zoning-districts.geojson")
zoning = zoning[['zoning', 'districtname', 'gen', 'geometry']].rename(columns={
    'zoning': 'current_zoning',
    'districtname': 'current_zoning_name',
    'gen': 'zoning_category'
})
print(f"  Loaded {len(zoning)} zoning districts")

print("\nLoading proposed rezoning (June 2025)...")
proposed = gpd.read_file(DATA_DIR / "rezone-proposed-2025-06.geojson")
proposed = proposed[['mapblklot', 'NEW_HEIGHT', 'gen_hght']].rename(columns={
    'NEW_HEIGHT': 'proposed_height',
    'gen_hght': 'proposed_height_num'
})
proposed = proposed.drop(columns=['geometry'])
print(f"  Loaded {len(proposed)} proposed rezoning parcels")

print("\nLoading neighborhoods...")
neighborhoods = gpd.read_file(DATA_DIR / "neighborhoods.geojson")
neighborhoods = neighborhoods[['nhood', 'geometry']]
print(f"  Loaded {len(neighborhoods)} neighborhoods")

print("\nEnsuring CRS compatibility...")
target_crs = parcels.crs
heights = heights.to_crs(target_crs)
zoning = zoning.to_crs(target_crs)
neighborhoods = neighborhoods.to_crs(target_crs)

print("\nPerforming spatial join: parcels <- heights (using centroid)...")
parcel_centroids = parcels.copy()
parcel_centroids['geometry'] = parcel_centroids.geometry.centroid
result = gpd.sjoin(parcel_centroids, heights, how='left', predicate='within')
result = result.drop(columns=['index_right'])
result['geometry'] = parcels.geometry
print(f"  Joined {result['current_height_num'].notna().sum()} parcels with height data")

print("\nPerforming spatial join: parcels <- zoning (using centroid)...")
result_centroids = result.copy()
result_centroids['geometry'] = result_centroids.geometry.centroid
result = gpd.sjoin(result_centroids, zoning, how='left', predicate='within')
result = result.drop(columns=['index_right'])
result['geometry'] = parcels.geometry
print(f"  Joined {result['current_zoning'].notna().sum()} parcels with zoning data")

print("\nPerforming spatial join: parcels <- neighborhoods (using centroid)...")
result_centroids = result.copy()
result_centroids['geometry'] = result_centroids.geometry.centroid
result = gpd.sjoin(result_centroids, neighborhoods, how='left', predicate='within')
result = result.drop(columns=['index_right'])
result['geometry'] = parcels.geometry
print(f"  Joined {result['nhood'].notna().sum()} parcels with neighborhood data")

print("\nPerforming attribute join: parcels <- proposed rezoning...")
result = result.merge(proposed, on='mapblklot', how='left')
print(f"  Joined {result['proposed_height'].notna().sum()} parcels with proposed rezoning")

print("\nSelecting and ordering final columns...")
final_columns = [
    'mapblklot',
    'Shape__Area',
    'Shape__Length',
    'nhood',
    'current_height_num',
    'current_height_code',
    'current_zoning',
    'current_zoning_name',
    'zoning_category',
    'proposed_height',
    'proposed_height_num',
    'geometry'
]

existing_columns = [col for col in final_columns if col in result.columns]
result = result[existing_columns]

print("\nCleaning data...")
result = result.drop_duplicates(subset=['mapblklot'])
print(f"  Final parcel count: {len(result)}")

print(f"\nExporting combined data to {OUTPUT_PATH}...")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
result.to_file(OUTPUT_PATH, driver='GeoJSON')

print(f"\n✅ Success! Combined GeoJSON saved to: {OUTPUT_PATH}")
print(f"   File size: {OUTPUT_PATH.stat().st_size / 1024 / 1024:.1f} MB")
print(f"   Total parcels: {len(result)}")
print(f"\nSample data:")
print(result[['mapblklot', 'nhood', 'current_height_num', 'proposed_height']].head(10))
