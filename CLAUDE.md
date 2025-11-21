# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a San Francisco rezoning analysis tool built as a client-side web application using Vue.js. It allows users to visualize and analyze the impact of various rezoning scenarios on housing development potential across SF parcels.

**Key Features:**
- Interactive map of SF parcels with Mapbox GL JS
- Three zoning layers: Original, Proposed (June 2025), User's Custom
- Attribute-based parcel filtering and selection
- Floor/unit calculation for different zoning scenarios
- Client-side only (no server, static hosting)

## Running the Application

### Local Development

From the `web-app` directory:

```bash
npm install
npm run dev
```

The app will open at http://localhost:5173

### Environment Setup

1. Copy `.env.example` to `.env`
2. Add your Mapbox token: `VITE_MAPBOX_TOKEN=pk.your_token_here`
3. Get a free token at https://account.mapbox.com/

### Build for Production

```bash
npm run build
```

Output will be in `dist/` directory, ready to deploy to any static hosting service (Netlify, Vercel, GitHub Pages, etc.).

## Architecture

### Technology Stack
- **Frontend**: Vue 3 + Vite
- **Mapping**: Mapbox GL JS
- **Data Processing**: Python (GeoPandas) or JavaScript (Turf.js)
- **Hosting**: Static (client-side only, no server)

### Data Flow

1. **Source data**: `data/` directory contains GeoJSON files for parcels, zoning, transit, neighborhoods, etc. (see `data/explanation.md`)
2. **Processing**: Python script (`scripts/combine_data.py`) combines source files into single GeoJSON
3. **App data**: `web-app/public/parcels_combined.geojson` - Single source of truth with all parcel attributes
4. **Frontend**: Vue.js loads combined GeoJSON and renders in Mapbox

### App Structure (`web-app/`)

```
web-app/
├── src/
│   ├── App.vue              - Root component
│   ├── components/
│   │   └── MapView.vue      - Map rendering component
│   └── main.js              - App entry point
├── public/
│   └── parcels_combined.geojson  - Combined parcel data (generated)
├── package.json
└── vite.config.js
```

### Data Processing (`scripts/`)

**`combine_data.py`** - Python script that combines source GeoJSON files:
- Loads parcel geometries
- Spatially joins current height limits (using centroid)
- Spatially joins current zoning districts (using centroid)
- Spatially joins neighborhoods (using centroid)
- Attribute join proposed rezoning by mapblklot
- Exports single combined GeoJSON file

Run: `python scripts/combine_data.py`

## Three Zoning Layers

The application tracks three zoning scenarios for each parcel:

1. **Original Zoning** - Current San Francisco zoning as of 2024:
   - `current_height_num` - Height limit (numeric, e.g., 40)
   - `current_height_code` - Height district code (e.g., "40-X")
   - `current_zoning` - Zoning code (e.g., "RH-2")
   - `current_zoning_name` - Full zoning name (e.g., "RESIDENTIAL- HOUSE, TWO FAMILY")

2. **Proposed Zoning** - June 2025 rezoning proposal (latest):
   - `proposed_height` - Proposed height (e.g., "85' Height Allowed")
   - `proposed_height_num` - Proposed height (numeric, e.g., 85)

3. **User's Custom Zoning** - User-defined via UI (stored in app state):
   - Users can select parcels and apply custom height limits
   - Calculated client-side

## Key Data Files

See `data/explanation.md` for complete documentation.

**Essential source files:**
- `parcels-all.geojson` (78MB) - All parcel geometries
- `zoning-height-bulk.geojson` (5.1MB) - Current height limits
- `zoning-districts.geojson` (6.4MB) - Current zoning types
- `rezone-proposed-2025-06.geojson` (58MB) - June 2025 proposed rezoning (LATEST)
- `neighborhoods.geojson` (1.6MB) - Neighborhood boundaries

**Generated file:**
- `web-app/public/parcels_combined.geojson` - Combined parcel data (created by `scripts/combine_data.py`)

## Parcel Data Structure

Each parcel in `parcels_combined.geojson` has these properties:

```json
{
  "mapblklot": "1067034",
  "Shape__Area": 2999.99609375,
  "Shape__Length": 289.99976435887436,
  "nhood": "Russian Hill",
  "current_height_num": 40,
  "current_height_code": "40-X",
  "current_zoning": "RH-2",
  "current_zoning_name": "RESIDENTIAL- HOUSE, TWO FAMILY",
  "zoning_category": "Residential",
  "proposed_height": "85' Height Allowed",
  "proposed_height_num": 85
}
```

## Constants

- `building_efficiency_discount = 0.8` - Factor for buildable area vs lot size
- `typical_unit_size = 850` sq ft
- Special zoning categories: "Increased density up to four units", "Increased density up to six units", "Density decontrol, unchanged height"

## Development Workflow

1. **Update source data**: Place new GeoJSON files in `data/` directory
2. **Regenerate combined data**: Run `python scripts/combine_data.py`
3. **Test in dev mode**: Run `npm run dev` in `web-app/`
4. **Build for production**: Run `npm run build` in `web-app/`
5. **Deploy**: Upload `dist/` directory to static hosting

## Geospatial Notes

- All GeoJSON files use CRS EPSG:4326 (WGS84) for Mapbox compatibility
- Spatial joins use parcel centroids to handle non-convex polygons
- Parcels are uniquely identified by `mapblklot` (block/lot combination)
- Mapbox GL JS handles geometry rendering and user interactions

## Migration Status

This project was migrated from R Shiny to Vue.js. See `MIGRATION_PLAN.md` for details.

**Completed:**
- ✅ Phase 0: Display Map
- ✅ Phase 1: Add Parcels (data processing script created)

**In Progress:**
- [ ] Phase 1: Load combined parcel data with hover tooltips
- [ ] Phase 2: Interactive zoning editor UI
- [ ] Phase 3: Floor calculation & impact analysis
