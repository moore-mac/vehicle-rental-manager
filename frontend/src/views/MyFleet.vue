<script setup>
import { ref, computed, onMounted } from "vue";
import { useVehicleStore } from "@/stores/vehicle";
import Add from "@carbon/icons-vue/es/add/16";

const vehicleStore = useVehicleStore();

const columns = [
  { key: "vrm", label: "Registration", sortable: false },
  { key: "make", label: "Make", sortable: false },
  { key: "model", label: "Model", sortable: false },
  { key: "colour", label: "Colour", sortable: false },
  { key: "vin", label: "VIN", sortable: false },
  { key: "year", label: "Year", sortable: false },
  { key: "category", label: "Category", sortable: false },
  { key: "numberSeats", label: "Seats", sortable: false },
  { key: "dayRate", label: "Day Rate (£)", sortable: false },
  { key: "status", label: "Status", sortable: false },
  { key: "fuelEconomy", label: "MPG", sortable: false },
  { key: "branch", label: "Branch", sortable: false },
];

onMounted(() => {
  vehicleStore.fetchAll();
});

// reactive data
const rows = computed(() => vehicleStore.vehicles);
const rowsSelected = ref([]);

// helpers
function debounce(fn, delay = 400) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

const doSearch = (value) => {
  if (!value) {
    vehicleStore.fetchAll();
    return;
  }
  vehicleStore.searchVehicles({ query: value });
};

// handlers
const onSearch = debounce(doSearch, 400);

function onSort({ column, order }) {
  vehicleStore.sortBy(column, order); // TODO implement in store
}

function onRowSelectChanges(selectedRows) {
  rowsSelected.value = selectedRows;
}

// function onPagination({ page, pageSize }) {
//   vehicleStore.fetchPage({ page, pageSize });
// }

function onBatchDelete() {
  if (rowsSelected.value.length) {
    vehicleStore.batchRemoveVehicles(rowsSelected.value);
    rowsSelected.value = [];
  }
}

function onAddVehicle() {
  console.log("Add Vehicle Action Clicked"); // TODO implement
}
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

        <h1>My Fleet</h1>

        <cv-data-table
          @search="onSearch"
          @sort="onSort"
          :rows-selected="rowsSelected"
          @update:rows-selected="onRowSelectChanges"
          :expandingSearch="false"
          class="my-fleet-table"
        >
          <!-- Batch Actions -->
          <template #batch-actions>
            <cv-button @click="onBatchDelete" kind="danger">
              Delete Selected
            </cv-button>
          </template>

          <!-- Global Actions -->
          <template #actions>
            <cv-data-table-action
              @click="onAddVehicle"
              aria-label="compile"
              alt="compile"
            >
              <Add />
            </cv-data-table-action>
          </template>

          <!-- Table Headings -->
          <template #headings>
            <cv-data-table-heading
              v-for="col in columns"
              :key="col.key"
              :id="col.key"
              :heading="col.label"
              :name="col.key"
              :sortable="col.sortable"
            />
          </template>

          <!-- Table Rows -->
          <template #data>
            <cv-data-table-row
              v-for="row in rows"
              :id="row.id"
              :key="row.id"
              :value="row.id"
            >
              <cv-data-table-cell>{{ row.vrm }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.make }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.model }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.colour }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.vin }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.year }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.category }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.numberSeats }}</cv-data-table-cell>
              <cv-data-table-cell>£{{ row.dayRate }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.status }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.fuelEconomy }}</cv-data-table-cell>
              <cv-data-table-cell>{{ row.branch }}</cv-data-table-cell>
            </cv-data-table-row>
          </template>
        </cv-data-table>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<style scoped>
h1 {
  margin: 1rem 0;
}
.my-fleet-table {
  max-height: calc(100vh - 20rem);
  overflow: scroll;
}
</style>
