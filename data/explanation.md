# Data Files Explanation

This folder contains GeoJSON files for San Francisco parcels and geographic features. These files are used to build the rezoning visualization tool.

## Core Parcel Data

### `parcels-all.geojson` (78MB)
All parcels with fourplex/sixplex zoning from April 2024.

**Properties:**
- `OBJECTID`: Unique ID
- `mapblklot`: Parcel identifier
- `Shape__Area`: Area
- `Shape__Length`: Perimeter length

### `parcels-corner.geojson` (68MB)
Corner parcels in San Francisco that qualify for increased density (6 units instead of 4 under certain zoning).

**Properties:**
- `objectid`: Unique ID
- `mapblklot`: Parcel identifier (block/lot combination)
- `streetintersection`: Name of street intersection (if applicable)
- `st_area(shape)`: Area in square feet
- `st_length(shape)`: Perimeter length in feet

## Proposed Rezoning

### `rezone-proposed-2025-06.geojson` (58MB) - **June 2025 Proposal**
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

### `zoning-districts.geojson` (6.4MB)
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

### `zoning-height-bulk.geojson` (5.1MB)
Current height and bulk restrictions for San Francisco parcels.

**Properties:**
- `height`: Height limit code (e.g., "40-X", "65-A", "450-S")
- `gen_hght`: Simplified height value as number (e.g., 40, 65, 450)

### `zoning-special-use.geojson` (2.0MB)
Special use districts with additional regulations.

**Properties:**
- `name`: District name (e.g., "Priority Equity Geographies Special Use District")
- `objectid`: Unique ID

## Geographic Reference Layers

### `neighborhoods.geojson` (1.6MB)
San Francisco neighborhood boundaries for analysis.

**Properties:**
- `nhood`: Neighborhood name

### `supervisor-districts.geojson` (297KB)
SF Board of Supervisors district boundaries.

**Properties:**
- `supervisor`: Supervisor name
- `district`: District number

### `streets.geojson` (14MB)
San Francisco street network.

## Transit and Amenities

### `transit-caltrain.geojson` (31KB)
Caltrain station locations in San Francisco.

### `transit-bart.geojson` (24KB)
BART station locations.

### `parks.geojson` (1.3MB)
Parks and recreation areas.

### `schools.geojson` (33KB)
School locations.

## Data Usage Notes

For the web application, we need to combine:

1. **Parcel geometries** from one of:
   - `parcels-all.geojson` (has all parcels)
   - `parcels-corner.geojson` (corner parcels only)

2. **Current zoning** from:
   - `zoning-districts.geojson` (zoning type)
   - `zoning-height-bulk.geojson` (height limits)

3. **Proposed rezoning** from:
   - `rezone-proposed-2025-06.geojson` (June 2025 proposal - LATEST)

4. **Optional enrichment data**:
   - Neighborhoods
   - Transit distances
   - Parks, schools

The combined dataset should allow users to:
- View original zoning for each parcel
- View proposed zoning (June 2025)
- Modify zoning to create custom scenarios
- Calculate housing unit impacts
