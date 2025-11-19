## Migration Plan: R Shiny → Vue.js Web App (POC First)

**Technology Stack:** Vue 3 + Vite + Mapbox GL JS (JavaScript/Python for data processing, no R)

**Three Zoning Layers:**
1. **Original Zoning**: Current SF zoning (height limits, zoning districts)
2. **Proposed Zoning**: June 2025 rezoning proposal (latest)
3. **User's Custom Zoning**: User-defined zoning via UI

### Phase 0: Display Map ✅
1. ✅ Create POC directory structure with Vue 3 + Vite setup
2. ✅ Load San Francisco map via Mapbox GL JS
3. ✅ Basic map navigation controls

### Phase 1: Add Parcels (In Progress)
1. ✅ Overlay parcel geometries on Mapbox map
2. **[Next]** Create data processing script (Python or JavaScript) to combine:
   - Parcel geometries (`FourPlex6plexCorners_20240416.geojson`)
   - Current zoning data:
     - Height limits from `Zoning Map - Height and Bulk Districts_20240121.geojson`
     - Zoning districts from `Zoning Map - Zoning Districts.geojson`
   - Proposed zoning from `rezone_sites_4_2025.geojson` (June 2025)
   - Optional: neighborhoods, transit distances
3. **[Next]** Export combined data as single GeoJSON file
4. **[Next]** Load combined parcel data in map with hover tooltips showing:
   - Parcel ID (mapblklot)
   - Neighborhood
   - Current height limit
   - Proposed height limit
   - Lot size

### Phase 2: Interactive Zoning Editor
1. Build UI for attribute-based parcel selection:
   - Filter by neighborhood
   - Filter by current zoning type
   - Filter by lot size
   - Filter by transit distance
   - Select individual parcels via map click
2. Allow user to apply custom zoning to selected parcels:
   - Set height limit (dropdown or input)
   - Set density controls
3. Visual feedback:
   - Color parcels by zoning layer (original/proposed/custom)
   - Show affected parcels highlighted

### Phase 3: Floor Calculation & Impact Analysis
1. Calculate floors allowed for each parcel under three scenarios:
   - Original zoning
   - Proposed zoning (June 2025)
   - User's custom zoning
2. Display summary statistics:
   - Total floors difference
   - Total housing units difference
   - Parcels affected count
3. Export results as CSV or JSON

## Data Processing Strategy

All data munging will use **JavaScript or Python** (no R):

1. **JavaScript approach** (recommended for web app):
   - Use Turf.js for spatial joins
   - Process GeoJSON files client-side or via Node.js script
   - Smaller bundle size

2. **Python approach** (alternative):
   - Use GeoPandas for spatial operations
   - Export combined GeoJSON for web app
   - Better for complex spatial operations

## Key Data Files

See `data/explanation.md` for detailed documentation of all GeoJSON files.

**Essential files:**
- `FourPlex6plexCorners_20240416.geojson` - All parcels
- `Zoning Map - Height and Bulk Districts_20240121.geojson` - Current height limits
- `Zoning Map - Zoning Districts.geojson` - Current zoning types
- `rezone_sites_4_2025.geojson` - June 2025 proposed rezoning (LATEST)
- `Analysis Neighborhoods_20240202.geojson` - Neighborhood boundaries
