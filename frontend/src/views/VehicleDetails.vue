<script setup>
import { onMounted, computed, watch, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useVehicleStore } from "@/stores/vehicle";

const route = useRoute();
const router = useRouter();
const vehicleStore = useVehicleStore();

const selectedVehicle = computed(() => vehicleStore.selectedVehicle);

onMounted(async () => {
  await fetchVehicle(route.query?.vrm || "");
});

onUnmounted(() => {
  localStorage.removeItem("previousRouteQuery");
});

watch(
  () => route.query,
  async (newQuery) => {
    await fetchVehicle(newQuery?.vrm || "");
  },
  { deep: true }
);

function goBack() {
  const savedQuery = localStorage.getItem("previousRouteQuery");
  let query = {};

  if (savedQuery) {
    try {
      query = JSON.parse(savedQuery);
    } catch (e) {
      console.error("Invalid saved query:", e);
      query = {};
    }
  }

  if (query && Object.keys(query).length > 0) {
    router.push({
      path: "/results",
      query,
    });
  } else {
    router.push({ path: "/results" });
  }
}

async function fetchVehicle(vrm) {
  if (vrm) {
    vehicleStore.selectedVehicle = await vehicleStore.fetchByReg(vrm);
  }
}

async function handleRent(vehicle) {
  if (vehicle && vehicle.status === "AVAILABLE") {
    vehicleStore.selectedVehicle = (
      await vehicleStore.rentVehicle(vehicle.vrm)
    )?.data;
    alert("Vehicle rented successfully!");
  }
}
async function handleReturn(vehicle) {
  if (vehicle && vehicle.status === "RENTED") {
    vehicleStore.selectedVehicle = (
      await vehicleStore.returnVehicle(vehicle.vrm)
    )?.data;
    alert("Vehicle returned successfully!");
  }
}
</script>

<template>
  <cv-grid>
    <cv-row>
      <cv-column>
        <cv-breadcrumb :no-trailing-slash="false">
          <cv-breadcrumb-item @click="$router.push('/')"
            >Home</cv-breadcrumb-item
          >

          <cv-breadcrumb-item @click="goBack">Search</cv-breadcrumb-item>
        </cv-breadcrumb>

        <h1 class="page-title">{{ route.query?.vrm }}</h1>

        <p v-if="!selectedVehicle">Loading vehicle...</p>

        <div v-else class="vehicle-card">
          <h2 class="vehicle-title">
            {{ selectedVehicle?.make }} {{ selectedVehicle?.model }} ({{
              selectedVehicle?.year
            }})
          </h2>
          <p class="vehicle-subtitle">
            VRM: <strong>{{ selectedVehicle?.vrm }}</strong> · VIN:
            <strong>{{ selectedVehicle?.vin }}</strong>
          </p>

          <div class="vehicle-info">
            <div class="info-item">
              <p class="label">Branch:</p>
              <p class="value">{{ selectedVehicle?.branch }}</p>
            </div>
            <div class="info-item">
              <p class="label">Category:</p>
              <p class="value">{{ selectedVehicle?.category }}</p>
            </div>
            <div class="info-item">
              <p class="label">Colour:</p>
              <p class="value">{{ selectedVehicle?.colour }}</p>
            </div>
            <div class="info-item">
              <p class="label">Seats:</p>
              <p class="value">{{ selectedVehicle?.numberSeats }}</p>
            </div>
            <div class="info-item">
              <p class="label">Fuel Economy:</p>
              <p class="value">{{ selectedVehicle?.fuelEconomy }} L/100km</p>
            </div>
            <div class="info-item">
              <p class="label">Daily Rate:</p>
              <p class="value">£{{ selectedVehicle?.dayRate }}</p>
            </div>
            <div class="info-item">
              <p class="label">Status:</p>
              <p
                class="value status"
                :class="selectedVehicle?.status?.toLowerCase()"
              >
                {{ selectedVehicle?.status }}
              </p>
            </div>
          </div>
        </div>

        <cv-button-set>
          <cv-button
            kind="primary"
            :disabled="selectedVehicle?.status !== 'AVAILABLE'"
            @click="handleRent(selectedVehicle)"
            >Rent</cv-button
          >
          <cv-button
            kind="secondary"
            @click="handleReturn(selectedVehicle)"
            :disabled="selectedVehicle?.status !== 'RENTED'"
            >Return</cv-button
          >
        </cv-button-set>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<style scoped>
.page-title {
  margin-bottom: 1rem;
}

.vehicle-card {
  background: var(--cds-layer-01);
  padding: 2rem;
  margin-bottom: 2rem;
}

.vehicle-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.vehicle-subtitle {
  color: #666;
  margin-bottom: 1.5rem;
}

.vehicle-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 2rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
}

.label {
  font-weight: 500;
  color: #444;
}

.value {
  font-weight: 600;
  color: #222;
}

.status.available {
  color: green;
}
.status.damaged {
  color: red;
}
.status.maintenance {
  color: orange;
}
</style>
