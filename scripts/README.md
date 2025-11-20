# Data Processing Scripts

## Requirements

Install Python dependencies:

```bash
pip install geopandas pandas
```

## Scripts

### `combine_data.py`

Combines parcel geometries with zoning data to create a single source of truth GeoJSON file.

**Input files:**
- `data/FourPlex6plexCorners_20240416.geojson` - Parcel geometries
- `data/Zoning Map - Height and Bulk Districts_20240121.geojson` - Current height limits
- `data/Zoning Map - Zoning Districts.geojson` - Current zoning types
- `data/rezone_sites_4_2025.geojson` - June 2025 proposed rezoning
- `data/Analysis Neighborhoods_20240202.geojson` - Neighborhood boundaries

**Output:**
- `web-app/public/parcels_combined.geojson` - Combined parcel data with all attributes

**Run:**
```bash
python scripts/combine_data.py
```

**What it does:**
1. Loads all input GeoJSON files
2. Performs spatial joins (using parcel centroids):
   - Joins current height limits to parcels
   - Joins current zoning districts to parcels
   - Joins neighborhoods to parcels
3. Performs attribute join:
   - Joins proposed rezoning by mapblklot
4. Exports combined data as single GeoJSON file

**Output columns:**
- `mapblklot` - Parcel ID
- `Shape__Area` - Parcel area (sq ft)
- `Shape__Length` - Parcel perimeter (ft)
- `nhood` - Neighborhood name
- `current_height_num` - Current height limit (numeric)
- `current_height_code` - Current height district code
- `current_zoning` - Current zoning code
- `current_zoning_name` - Current zoning name
- `zoning_category` - General zoning category
- `proposed_height` - Proposed height limit (text)
- `proposed_height_num` - Proposed height limit (numeric)
- `geometry` - Parcel geometry
