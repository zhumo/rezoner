# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a San Francisco rezoning analysis tool built as a Shiny web application. It allows users to visualize and analyze the impact of various rezoning scenarios on housing development potential across SF parcels.

## Running the Application

### Local Development
In RStudio, open `rezoner/app.R` and click 'Run App'. The app requires these packages:
```r
required_packages <- c("shiny", "dplyr", "sf", "shinyjs", "shinyBS", "mapboxer", "sortable", "shinyWidgets", "stringr", "viridis", "compiler", "RColorBrewer")
```

If package installation fails, use: `install.packages('package_name', type='source')`

You do NOT need to source `main.R` to run the webapp. The required RDS files (`light_model.rds`, `sf_map.rds`, `five_rezonings_nongeo.rds`) are included in the repository.

### Reproducing Data Pipeline
To regenerate the RDS files that power the app:

1. Install git-lfs and run `git lfs pull`
2. Install additional packages: `readr`, `readxl`, `tidyr`, `modelr`, `caret`, `sfarrow`, `rmapshaper`, `tidytransit`, `doParallel`, `lwgeom`
3. Source `main.R` (may take over 1 hour depending on CPU cores)

The pipeline in `main.R` executes in sequence:
1. `merge_scenario_d.R` - Loads and merges multiple rezoning scenario GeoJSON files (Fall 2023, Jan 2024, May 2025) with parcel data
2. `preprocessing.R` - Joins spatial data (heights, transit distances, AFFH scores, etc.) to parcels using centroid joins and parallelized nearest-neighbor calculations
3. `filter_out_extraneous.R` - Filters dataset to relevant parcels
4. `to_mapbox.R` - Converts processed data to Mapbox-compatible format

## Architecture

### Data Flow
- **Source data**: `data/` directory contains GeoJSON files for parcels, zoning, transit, neighborhoods, etc.
- **Processing pipeline**: `main.R` orchestrates the sequential processing steps
- **App data**: Three RDS files in `rezoner/` directory:
  - `five_rezonings_nongeo.RDS` - Full parcel data without geometries (for calculations)
  - `sf_map.RDS` - Spatial data for map visualization
  - `light_model.rds` - Statistical model for predicting housing units

### App Structure (`rezoner/`)
- `app.R` - Main application logic and server functions
- `ui.R` - Shiny UI definition
- `modules.R` - Reusable Shiny modules
- `utils.R` - Utility functions for color palettes and text conversion

### Key Functions

**`update_df_()` in `app.R`** - Core function that calculates the effect of rezoning scenarios on housing unit predictions. Modify this to change how rezoning impacts are calculated.

**`yimbycity()` in `app.R`** - Example custom rezoning function that demonstrates parcel-level zoning using block/lot combinations. Use as pattern for defining custom rezonings with greater resolution than the UI allows.

**`union_of_maxdens()` in `app.R`** - Takes the maximum density across all rezoning scenarios (M1-M5) for each parcel.

**`get_denser_zone()` in `app.R`** - Compares zoning by extracting numeric height values and returns the more permissive zoning.

**`centroid_join()` in `preprocessing.R`** - Spatially joins auxiliary data to parcels using point-on-surface (handles non-convex polygons better than true centroids).

**`parallelize_nearest()` in `preprocessing.R`** - Parallelized nearest-neighbor distance calculations for transit/amenity proximity using multiple cores.

### Rezoning Data Structure
The app tracks five rezoning scenarios (M1-M5):
- M1, M2, M3: Earlier rezoning proposals
- M4: Fall 2023 rezoning (`Fall2023Rezoning.json`)
- M5: January 2024 rezoning (`rezone_sites_1_2024.geojson`)
- M6: May 2025 rezoning (`data/rezone_sites_5_2025.geojson`) with base and local variants

Each scenario defines `ZONING` (e.g., "85' Height Allowed") and height values for parcels.

### Spatial Data Integration
`preprocessing.R` joins these datasets to parcels:
- Height and bulk districts
- Transit distances (BART, Caltrain, MUNI rapid)
- AFFH (Affirmatively Furthering Fair Housing) opportunity scores
- Commercial corridors
- Parks, schools, and other amenities
- Development pipeline data
- Supervisor districts

## Constants
- `building_efficiency_discount = 0.8` - Factor for buildable area vs lot size
- `typical_unit_size = 850` sq ft
- Special zoning categories: "Increased density up to four units", "Increased density up to six units", "No height change, density decontrol", "300' Height Allowed"

## Debugging
Use `browser()` to set breakpoints in the code. The app runs with `options(shiny.fullstacktrace=TRUE)` for detailed error traces.

## Geospatial Notes
- CRS transformations ensure all datasets align with the base parcel layer
- `sf_use_s2(F)` disables spherical geometry for faster planar operations
- Parcels are identified by `mapblklot` (block/lot combination) visible in map popups
