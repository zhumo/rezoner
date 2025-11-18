<script setup>
import { onMounted, ref } from 'vue';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

const mapContainer = ref(null);
const map = ref(null);

onMounted(() => {
  mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

  map.value = new mapboxgl.Map({
    container: mapContainer.value,
    style: 'mapbox://styles/mapbox/light-v11',
    center: [-122.4194, 37.7749],
    zoom: 12,
    minZoom: 10,
    maxZoom: 18,
    maxBounds: [
      [-122.55, 37.65],
      [-122.28, 37.85]
    ]
  });

  map.value.addControl(new mapboxgl.NavigationControl(), 'top-right');

  map.value.on('load', async () => {
    const response = await fetch('/parcels.geojson');
    const parcels = await response.json();

    map.value.addSource('parcels', {
      type: 'geojson',
      data: parcels
    });

    map.value.addLayer({
      id: 'parcels-fill',
      type: 'fill',
      source: 'parcels',
      paint: {
        'fill-color': '#088',
        'fill-opacity': 0.4
      }
    });

    map.value.addLayer({
      id: 'parcels-outline',
      type: 'line',
      source: 'parcels',
      paint: {
        'line-color': '#000',
        'line-width': 0.5,
        'line-opacity': 0.2
      }
    });

    console.log(`Loaded ${parcels.features.length} parcels`);
  });
});
</script>

<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
}
</style>
