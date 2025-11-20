# Data Files Explanation

This folder contains GeoJSON files for San Francisco parcels and geographic features. These files are used to build the rezoning visualization tool.

## Core Parcel Data

### `Parcels_Corner.geojson` (68MB)
Corner parcels in San Francisco that qualify for increased density (6 units instead of 4 under certain zoning).

**Properties:**
- `objectid`: Unique ID
- `mapblklot`: Parcel identifier (block/lot combination)
- `streetintersection`: Name of street intersection (if applicable)
- `st_area(shape)`: Area in square feet
- `st_length(shape)`: Perimeter length in feet

### `FourPlex6plexCorners_20240416.geojson` (78MB)
All parcels with fourplex/sixplex zoning from April 2024.

**Properties:**
- `OBJECTID`: Unique ID
- `mapblklot`: Parcel identifier
- `Shape__Area`: Area
- `Shape__Length`: Perimeter length

### `fourplex_areas_12_2023.geojson` (133B)
Legacy fourplex areas from December 2023 (stub file).

## Proposed Rezoning

### `rezone_sites_4_2025.geojson` (58MB) - **June 2025 Proposal**
Rezoning proposal from June 2025 (latest).

**Properties:**
- `OBJECTID`: Unique ID
- `mapblklot`: Parcel identifier
- `NEW_HEIGHT`: Proposed height limit (e.g., "40' Height Allowed", "85' Height Allowed", "Density decontrol, unchanged height")
- `height`: Existing height district code (e.g., "40-X")
- `gen_hght`: Existing height as numeric value (e.g., 40)
- `Shape__Area`: Area in square feet
- `Shape__Length`: Perimeter length

## Current Zoning

### `Zoning Map - Zoning Districts.geojson` (6.4MB)
Current zoning districts for San Francisco.

**Properties:**
- `zoning`: Zoning code (e.g., "RH-2", "RM-1")
- `districtname`: Full district name (e.g., "RESIDENTIAL- HOUSE, TWO FAMILY")
- `gen`: General category (e.g., "Residential", "Commercial")
- `commercial_hours_of_operation`: Hours for commercial zones
- `codesection`: Planning code section reference
- `url`: Link to planning code
- `objectid`: Unique ID
- `shape_area`, `shape_length`: Geometry measurements

### `Zoning Map - Height and Bulk Districts_20240121.geojson` (5.1MB)
Current height and bulk restrictions for San Francisco parcels.

**Properties:**
- `height`: Height limit code (e.g., "40-X", "65-A", "450-S")
- `gen_hght`: Simplified height value as number (e.g., 40, 65, 450)

### `Zoning Map - Special Use Districts_20240122.geojson` (2.0MB)
Special use districts with additional regulations.

**Properties:**
- `name`: District name (e.g., "Priority Equity Geographies Special Use District")
- `objectid`: Unique ID

## Geographic Reference Layers

### `Analysis Neighborhoods_20240202.geojson` (1.6MB)
San Francisco neighborhood boundaries for analysis.

**Properties:**
- `nhood`: Neighborhood name

### `Supervisor Districts (2022)_20240124.geojson` (297KB)
SF Board of Supervisors district boundaries.

**Properties:**
- `supervisor`: Supervisor name
- `district`: District number

### `Streets   Active and Retired_20240331.geojson` (14MB)
San Francisco street network.

## Transit and Amenities

### `Caltrain Stations and Stops.geojson` (31KB)
Caltrain station locations in San Francisco.

### `BART_System_2020/BART_Station.geojson` (24KB)
BART station locations.

### `Park Lands - Recreation and Parks Department.geojson` (1.3MB)
Parks and recreation areas.

### `Schools_College_20240215.geojson` (33KB)
School locations.

## Data Usage Notes

For the web application, we need to combine:

1. **Parcel geometries** from one of:
   - `FourPlex6plexCorners_20240416.geojson` (has all parcels)
   - `Parcels_Corner.geojson` (corner parcels only)

2. **Current zoning** from:
   - `Zoning Map - Zoning Districts.geojson` (zoning type)
   - `Zoning Map - Height and Bulk Districts_20240121.geojson` (height limits)

3. **Proposed rezoning** from:
   - `rezone_sites_4_2025.geojson` (June 2025 proposal - LATEST)

4. **Optional enrichment data**:
   - Neighborhoods
   - Transit distances
   - Parks, schools

The combined dataset should allow users to:
- View original zoning for each parcel
- View proposed zoning (June 2025)
- Modify zoning to create custom scenarios
- Calculate housing unit impacts
