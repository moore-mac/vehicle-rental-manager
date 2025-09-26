<script setup>
import { ref, computed, onMounted } from "vue";
import { useVehicleStore } from "@/stores/vehicle";
import Add from "@carbon/icons-vue/es/add/16";
import SideBarFilter from "@/components/SideBarFilter.vue";
import { useRouter } from "vue-router";

import useVuelidate from "@vuelidate/core";
import { required } from "@vuelidate/validators";

const vehicleStore = useVehicleStore();
const router = useRouter();

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

onMounted(async () => {
  await vehicleStore.fetchAll();
});

// reactive data
const rows = computed(() => vehicleStore.vehicles);
const rowsSelected = ref([]);
const showAddModal = ref(false);
const newVehicle = ref({
  make: "",
  model: "",
  colour: "",
  vin: "",
  year: null,
  vrm: "",
  category: "",
  numberSeats: 1,
  dayRate: 0,
  status: "AVAILABLE",
  fuelEconomy: 0,
  branch: "",
});
const query = ref("");

// validation
const rules = {
  make: { required },
  model: { required },
  colour: { required },
  vin: { required },
  year: { required },
  vrm: { required },
  category: { required },
  numberSeats: { required },
  dayRate: { required },
  status: { required },
  fuelEconomy: { required },
  branch: { required },
};

const v$ = useVuelidate(rules, newVehicle);

// helpers
function debounce(fn, delay = 400) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

const doSearch = (value) => {
  query.value = value;

  const params = {
    ...vehicleStore.filters,
    query: query.value,
  };

  Object.keys(params).forEach((key) => {
    if (
      params[key] === undefined ||
      params[key] === null ||
      params[key] === ""
    ) {
      delete params[key];
    }
  });

  vehicleStore.searchVehicles(params);
};

// handlers
const onSearch = debounce(doSearch, 400);

function onRowSelectChanges(selectedRows) {
  rowsSelected.value = selectedRows;
}

function onBatchDelete() {
  if (rowsSelected.value.length) {
    vehicleStore.batchRemoveVehicles(rowsSelected.value);
    rowsSelected.value = [];
  }
}

function onAddVehicle() {
  v$.value.$touch();
  if (!v$.value.$invalid) {
    vehicleStore.addVehicle(newVehicle.value);
    showAddModal.value = false;
    router.push(`/vehicles?vrm=${newVehicle.value.vrm}`);
  }
}

function onAfterModalHidden() {
  showAddModal.value = false;
  v$.value.$reset();
}

async function onFiltersChanged(filters) {
  const params = { ...filters, query: query.value };

  Object.keys(params).forEach((key) => {
    if (
      params[key] === undefined ||
      params[key] === null ||
      params[key] === ""
    ) {
      delete params[key];
    }
  });

  await vehicleStore.searchVehicles(params);
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

        <h1>My Fleet</h1>
        <p>{{ rows.length }} vehicles found</p>
      </cv-column>
    </cv-row>

    <cv-row>
      <cv-column :lg="4" :md="3" :sm="4">
        <SideBarFilter @update:filters="onFiltersChanged" />
      </cv-column>

      <cv-column :lg="8" :md="5" :sm="4">
        <cv-data-table
          @search="onSearch"
          @sort="() => {}"
          :rows-selected="rowsSelected"
          @update:rows-selected="onRowSelectChanges"
          :expandingSearch="false"
          class="my-fleet-table"
        >
          <template #batch-actions>
            <cv-button @click="onBatchDelete" kind="danger">
              Delete Selected
            </cv-button>
          </template>

          <template #actions>
            <cv-data-table-action @click="showAddModal = true">
              <Add />
            </cv-data-table-action>
          </template>

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

  <cv-modal
    :visible="showAddModal"
    size="md"
    :hasFormContent="true"
    @after-modal-hidden="onAfterModalHidden"
    @primary-click="onAddVehicle"
    @secondary-click="onAfterModalHidden"
  >
    <template #label>Vehicle Form Modal</template>
    <template #title>Add a New Vehicle</template>
    <template #content>
      <cv-form
        @submit.prevent=""
        style="display: flex; flex-direction: column; gap: 1rem"
      >
        <cv-text-input
          label="Vehicle Registration *"
          v-model="newVehicle.vrm"
          :invalid-message="
            v$.vrm.$error ? 'Registration Number is required' : ''
          "
          placeholder="e.g., AW69DVJ"
        />

        <cv-text-input
          label="Make *"
          v-model="newVehicle.make"
          :invalid-message="v$.make.$error ? 'Vehicle Make is required' : ''"
          placeholder="e.g., Ford"
        />

        <cv-text-input
          label="Model *"
          v-model="newVehicle.model"
          :invalid-message="v$.model.$error ? 'Vehicle Model is required' : ''"
          placeholder="e.g., Fiesta"
        />

        <cv-text-input
          label="Colour *"
          v-model="newVehicle.colour"
          :invalid-message="v$.colour.$error ? 'Colour is required' : ''"
          placeholder="e.g., Grey"
        />

        <cv-text-input
          label="VIN *"
          v-model="newVehicle.vin"
          :invalid-message="v$.vin.$error ? 'VIN is required' : ''"
          placeholder="e.g., B2IJ49B2B3UYIANSI"
        />

        <cv-number-input
          label="Year *"
          v-model="newVehicle.year"
          :invalid-message="
            v$.year.$error ? 'Year is required and must be >= 1900' : ''
          "
          min="1900"
        />

        <cv-combo-box
          title="Category *"
          label="e.g., SUV, compact, etc."
          :options="vehicleStore.categoryOptions"
          v-model="newVehicle.category"
          :invalid-message="v$.category.$error ? 'Category is required' : ''"
          :is-light="true"
        />

        <cv-number-input
          label="Seats *"
          v-model="newVehicle.numberSeats"
          :invalid-message="
            v$.numberSeats.$error ? 'Seats are required and must be > 0' : ''
          "
          min="1"
        />

        <cv-number-input
          label="Day Rate (£) *"
          v-model="newVehicle.dayRate"
          :invalid-message="
            v$.dayRate.$error ? 'Day Rate is required and must be >= 0' : ''
          "
          min="0"
        />

        <cv-combo-box
          title="Status *"
          label="Available, Rented, Maintenance"
          :options="vehicleStore.statusOptions"
          v-model="newVehicle.status"
          :invalid-message="v$.status.$error ? 'Status is required' : ''"
          :is-light="true"
        />

        <cv-number-input
          label="Fuel Economy (MPG) *"
          v-model="newVehicle.fuelEconomy"
          :invalid-message="
            v$.fuelEconomy.$error
              ? 'Fuel Economy is required and must be >= 0'
              : ''
          "
          min="0"
        />

        <cv-combo-box
          title="Branch *"
          label="London, Bristol, etc."
          :options="vehicleStore.branchOptions"
          v-model="newVehicle.branch"
          :invalid-message="v$.branch.$error ? 'Branch is required' : ''"
          :is-light="true"
          style="margin-bottom: 4rem"
        />
      </cv-form>
    </template>
    <template #secondary-button>Close</template>
    <template #primary-button>Add</template>
  </cv-modal>
</template>

<style scoped>
.my-fleet-table {
  max-height: calc(100vh - 20rem);
  overflow: scroll;
}
</style>
