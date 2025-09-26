<script setup>
import { watch, onMounted } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";
import { useVehicleStore } from "@/stores/vehicle";

const emit = defineEmits(["update:filters"]);
const route = useRoute();
const vehicleStore = useVehicleStore();

onMounted(async () => {
  await vehicleStore.fetchBranches();
  await vehicleStore.fetchCategories();
  await vehicleStore.fetchStatuses();

  const filters = {};
  const { category, status, branch } = route.query;

  if (category && vehicleStore.categories.includes(category))
    filters.category = category;
  if (status && vehicleStore.statuses.includes(status)) filters.status = status;
  if (branch && vehicleStore.branches.includes(branch)) filters.branch = branch;

  vehicleStore.filters = filters;
});

onBeforeRouteLeave(() => {
  vehicleStore.filters = {};
});

watch(
  () => vehicleStore.filters,
  (newFilters) => {
    emit("update:filters", newFilters);
  },
  { deep: true }
);
</script>

<template>
  <div class="sidebar">
    <h4>Filters</h4>

    <cv-combo-box
      title="Category"
      label="e.g., SUV, compact, etc."
      :options="vehicleStore.categoryOptions"
      v-model="vehicleStore.filters.category"
      :is-light="false"
    />

    <cv-combo-box
      title="Status"
      label="Available, Rented, etc."
      :options="vehicleStore.statusOptions"
      v-model="vehicleStore.filters.status"
      :is-light="false"
    />

    <cv-combo-box
      title="Branch"
      label="London, Bristol, etc."
      :options="vehicleStore.branchOptions"
      v-model="vehicleStore.filters.branch"
      :is-light="false"
    />
  </div>
</template>

<style scoped>
.sidebar {
  border-right: 1px solid var(--cds-border-subtle-01);
  padding: 0 2rem 2rem 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
}
</style>
