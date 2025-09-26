<script setup>
import { onMounted, computed } from "vue";
import { onBeforeRouteLeave, useRoute, useRouter } from "vue-router";
import { useVehicleStore } from "@/stores/vehicle";
import SideBarFilter from "@/components/SideBarFilter.vue";

const router = useRouter();
const route = useRoute();

const vehicleStore = useVehicleStore();
const results = computed(() => vehicleStore.vehicles);

onMounted(async () => {
  await vehicleStore.searchVehicles(route.query);
});

onBeforeRouteLeave(() => {
  localStorage.setItem("previousRouteQuery", JSON.stringify(route.query));
});

function viewDetails(vehicle) {
  router.push({ path: "/vehicles", query: { vrm: vehicle.vrm } });
}

async function onFiltersChanged(filters) {
  await vehicleStore.searchVehicles(filters);
}
</script>

<template>
  <cv-grid>
    <cv-row style="margin-bottom: 1rem">
      <cv-column>
        <cv-breadcrumb :no-trailing-slash="false">
          <cv-breadcrumb-item @click="$router.push('/')">
            Home
          </cv-breadcrumb-item>
        </cv-breadcrumb>

        <h1>Search Results</h1>
        <p>{{ results.length }} vehicles found</p>
      </cv-column>
    </cv-row>

    <cv-row class="search-results-row">
      <cv-column>
        <div class="loading-wheel" v-if="!results || results.length === 0">
          <cv-loading description="Loading vehicles..." />
        </div>

        <div v-else>
          <cv-row>
            <cv-column :lg="4" :md="3" :sm="4">
              <SideBarFilter @update:filters="onFiltersChanged" />
            </cv-column>
            <cv-column class="results-tile-container" :lg="8" :md="5" :sm="4">
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
                <p>Registration: {{ vehicle.vrm }}</p>
                <cv-tag
                  style="cursor: pointer"
                  :kind="vehicleStore.statusColourMap[vehicle.status]"
                  :label="vehicleStore.statusLabelMap[vehicle.status]"
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
.results-tile-container {
  margin-top: 1rem;
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
