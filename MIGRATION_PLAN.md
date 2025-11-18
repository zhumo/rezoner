## Migration Plan: R Shiny → Vue.js Web App (POC First)

### Phase 0: Display Map
1. **Create POC directory structure** with Vue 3 + Vite setup
2. In the Vue page, by default load a map of San Francisco via mapbox

### Phase 1: Add parcels
1. Generate the list of parcels (no parcel data necessary, just shape)
2. Overlay that list of parcels on top of the SF mapbox

### Phase 2: Allow selection by parcel attribute
1. Each parcel data attribute should be associated with various attributes
2. In the UI, allow the user to select various attributes and apply a max floors.
3. The system should then calculate the current # floors allowed on each parcel then sum up the difference, giving a total sum given the new policy
