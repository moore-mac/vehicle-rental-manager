<script setup>
import { onMounted, ref } from "vue";
import { useVehicleStore } from "@/stores/vehicle";
import StatusByBranch from "@/components/charts/StatusByBranch.vue";
import CategoryByBranch from "@/components/charts/CategoryByBranch.vue";
import RentalUtilisationByBranch from "@/components/charts/RentalUtilisationByBranch.vue";
import RentedByCategory from "@/components/charts/RentedByCategory.vue";
import VehiclesWithIssues from "@/components/charts/VehiclesWithIssues.vue";
import FleetDashboard from "@/components/charts/FleetDashboard.vue";

const vehicleStore = useVehicleStore();

const selectedTabId = ref("");
const selectedBranch = ref("");

onMounted(async () => {
  await vehicleStore.fetchBranches();
  selectedBranch.value = vehicleStore.branchOptions[0].value;
});
</script>

<template>
  <cv-grid>
    <cv-row>
      <cv-column>
        <cv-breadcrumb :no-trailing-slash="false">
          <cv-breadcrumb-item @click="$router.push('/')">
            Home
          </cv-breadcrumb-item>
        </cv-breadcrumb>

        <h1 style="margin-bottom: 1rem">Analytics</h1>

        <cv-tabs>
          <cv-tab
            id="tab-1"
            label="Branch Manager"
            :selected="selectedTabId === 'tab-1'"
          >
            <br />
            <cv-combo-box
              title="Select a branch to view analytics dashboard from the perspective of a branch manager"
              label="City"
              :options="vehicleStore.branchOptions"
              v-model="selectedBranch"
              style="margin-bottom: 2rem"
            ></cv-combo-box>

            <div v-if="selectedBranch" class="analytics-dashboard">
              <VehiclesWithIssues :branch="selectedBranch" />
              <RentalUtilisationByBranch :branch="selectedBranch" />
              <StatusByBranch :branch="selectedBranch" />
              <CategoryByBranch :branch="selectedBranch" />
              <RentedByCategory :branch="selectedBranch" />
            </div>
          </cv-tab>

          <cv-tab
            id="tab-2"
            label="Fleet Owner"
            :selected="selectedTabId === 'tab-2'"
          >
            <FleetDashboard />
          </cv-tab>
        </cv-tabs>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<style scoped>
.analytics-dashboard {
  display: flex;
  flex-wrap: wrap;
  gap: 4rem;
  justify-content: flex-start;
  align-items: stretch;
}

.analytics-dashboard > * {
  flex: 1 1 25rem;
  min-width: 25rem;
  max-width: 35rem;
}
</style>
