<script setup>
import { onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useVehicleStore } from "@/stores/vehicle";

const router = useRouter();
const route = useRoute();

const vehicleStore = useVehicleStore();
const results = computed(() => vehicleStore.vehicles);

onMounted(async () => {
  try {
    if (!vehicleStore.vehicles.length) {
      await vehicleStore.fetchVehiclesByBranch(route.query.branch);
    }
  } catch (error) {
    console.log(error);
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
        <cv-heading level="1">Search Results</cv-heading>

        <!-- Loading -->
        <cv-loading
          v-if="!results || results.length === 0"
          description="Loading vehicles..."
        />

        <!-- Results -->
        <div v-else>
          <p class="results-summary">
            {{ results.length }} vehicles found in
            <strong>{{ route.query.branch }}</strong>
          </p>

          <cv-grid>
            <cv-row>
              <cv-column
                v-for="vehicle in results"
                :key="vehicle.vrm"
                sm="4"
                md="4"
                lg="8"
              >
                <cv-tile
                  kind="clickable"
                  @click="viewDetails(vehicle)"
                  class="vehicle-tile"
                >
                  <cv-heading level="3" class="vehicle-title">
                    {{ vehicle.make }} {{ vehicle.model }}
                  </cv-heading>
                  <p class="vehicle-subtitle">
                    Year: {{ vehicle.year }} · Seats: {{ vehicle.numberSeats }}
                  </p>
                  <p class="vehicle-branch">Branch: {{ vehicle.branch }}</p>
                  <cv-tag
                    :type="
                      vehicle.status === 'AVAILABLE'
                        ? 'green'
                        : vehicle.status === 'DAMAGED'
                          ? 'red'
                          : 'warm-gray'
                    "
                  >
                    {{ vehicle.status }}
                  </cv-tag>
                </cv-tile>
              </cv-column>
            </cv-row>
          </cv-grid>
        </div>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<style scoped>
.search-results-row {
  margin-bottom: 4rem;
}

.results-summary {
  margin-bottom: 1.5rem;
  font-size: 1rem;
  color: #525252;
}

.vehicle-tile {
  margin-bottom: 1rem;
  padding: 1rem;
}

.vehicle-title {
  margin-bottom: 0.25rem;
}

.vehicle-subtitle {
  font-size: 0.875rem;
  color: #6f6f6f;
  margin-bottom: 0.25rem;
}

.vehicle-branch {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}
</style>
