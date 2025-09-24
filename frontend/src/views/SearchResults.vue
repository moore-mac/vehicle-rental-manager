<script setup>
import { onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useVehicleStore } from "@/stores/vehicle";

const router = useRouter();
const route = useRoute();

const vehicleStore = useVehicleStore();
const results = computed(() => vehicleStore.vehicles);

const statusColourMap = {
  AVAILABLE: "green",
  RENTED: "red",
  SERVICEREQ: "red",
  DAMAGED: "red",
};

const statusLabelMap = {
  AVAILABLE: "Available",
  RENTED: "Rented",
  SERVICEREQ: "Service Required",
  DAMAGED: "Damaged",
};

onMounted(async () => {
  try {
    let queryToUse = route.query;

    if (!queryToUse || Object.keys(queryToUse).length === 0) {
      const savedQuery = localStorage.getItem("previousRouteQuery");
      if (savedQuery) {
        queryToUse = JSON.parse(savedQuery);
        router.replace({ path: "/results", query: queryToUse });
      }
    } else {
      localStorage.setItem("previousRouteQuery", JSON.stringify(queryToUse));
    }

    await vehicleStore.searchVehicles(queryToUse);
  } catch (error) {
    console.error("Failed to fetch vehicles:", error);
  }
});

function viewDetails(vehicle) {
  router.push({ path: "/vehicle", query: { vrm: vehicle.vrm } });
}
</script>

<template>
  <cv-grid>
    <cv-row class="search-results-row">
      <cv-column>
        <cv-breadcrumb :no-trailing-slash="false">
          <cv-breadcrumb-item @click="$router.push('/')">
            Home
          </cv-breadcrumb-item>
        </cv-breadcrumb>

        <h1>Search Results</h1>

        <!-- Loading -->
        <div class="loading-wheel" v-if="!results || results.length === 0">
          <cv-loading description="Loading vehicles..." />
        </div>

        <!-- Results -->
        <div v-else>
          <p class="results-summary">{{ results.length }} vehicles found</p>

          <cv-row>
            <cv-column class="results-tile-container">
              <cv-tile
                v-for="vehicle in results"
                :key="vehicle.vrm"
                kind="clickable"
                @click="viewDetails(vehicle)"
                class="vehicle-tile"
              >
                <h3 class="vehicle-title">
                  {{ vehicle.make }} {{ vehicle.model }}
                </h3>
                <p>
                  Year: {{ vehicle.year }} · Seats: {{ vehicle.numberSeats }}
                </p>
                <p>Branch: {{ vehicle.branch }}</p>
                <cv-tag
                  style="cursor: pointer"
                  :kind="statusColourMap[vehicle.status]"
                  :label="statusLabelMap[vehicle.status]"
                />
              </cv-tile>
            </cv-column>
          </cv-row>
        </div>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<style scoped>
.search-results-row {
  margin-bottom: 4rem;
}
.loading-wheel {
  position: absolute;
  top: 40%;
  left: 45%;
}
.results-summary {
  margin-bottom: 1.5rem;
  font-size: 1rem;
  color: #525252;
}
.results-tile-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
.vehicle-tile {
  margin-bottom: 1rem;
  padding: 1rem;
  height: 100%;
}
.veicle-title {
  margin-bottom: 0.25rem;
}
</style>
