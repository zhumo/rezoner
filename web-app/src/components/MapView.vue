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
