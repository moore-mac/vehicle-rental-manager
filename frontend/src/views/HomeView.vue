<script setup>
import CheckMark16 from "@carbon/icons-vue/es/checkmark--outline/16";
import Car from "@carbon/icons-vue/es/car/16";
import IBMSecurity from "@carbon/icons-vue/es/ibm-security/16";
import Time from "@carbon/icons-vue/es/time/16";

import { onMounted, computed, ref } from "vue";
import { useVehicleStore } from "@/stores/vehicle";
import { useRouter } from "vue-router";

import useVuelidate from "@vuelidate/core";
import { required } from "@vuelidate/validators";

const router = useRouter();
const vehicleStore = useVehicleStore();

const selectedBranch = ref(null);
const dateRange = ref([null, null]);
const driverOver25 = ref(false);

const rules = {
  selectedBranch: { required },
};

const v$ = useVuelidate(rules, { selectedBranch });

onMounted(() => {
  vehicleStore.fetchBranches();
  vehicleStore.fetchCategories();
});

const branchOptions = computed(() =>
  vehicleStore.branches.map((branch, index) => ({
    name: `branch-${index + 1}`,
    label: branch,
    value: branch,
  }))
);

async function handleSubmit() {
  v$.value.$touch();
  if (!v$.value.$invalid) {
    try {
      router.push({
        path: "/results",
        query: { branch: selectedBranch.value },
      });
    } catch (error) {
      console.log(error);
    }
  }
}

async function handleCategorySearch(category) {
  try {
    router.push({
      path: "/results",
      query: { category },
    });
  } catch (error) {
    console.log(error);
  }
}

const scrollToId = (id) => {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: "smooth" });
  }
};
</script>

<template>
  <cv-grid style="overflow: hidden">
    <img
      class="landing-hero-background"
      src="/src/assets/landing-hero.jpg"
      alt="landing hero background"
    />

    <cv-row class="landing-hero-row">
      <cv-column :lg="{ span: 6, offset: 6 }" :md="8" :sm="4">
        <cv-form @submit.prevent="" class="landing-form">
          <h1>Find a Ride</h1>
          <cv-combo-box
            title="Collect From *"
            label="City"
            :options="branchOptions"
            v-model="selectedBranch"
            :invalid-message="
              v$.selectedBranch.$error ? 'Branch is required' : ''
            "
          ></cv-combo-box>

          <!-- TODO add selected category -->

          <cv-date-picker
            dateLabel="Date From"
            dateEndLabel="Date To"
            :cal-options="{ dateFormat: 'd/m/Y' }"
            placeholder="dd-mm-yyyy"
            kind="range"
            v-model="dateRange"
          ></cv-date-picker>

          <cv-checkbox
            label="Driver aged over 25"
            value="yes"
            v-model="driverOver25"
            :inline="true"
          ></cv-checkbox>

          <div>
            <cv-button kind="primary" @click="handleSubmit()">Submit</cv-button>

            <cv-button kind="tertiary" @click="scrollToId('why-choose-us')"
              >Why Choose Us?</cv-button
            >
          </div>
        </cv-form>
      </cv-column>
    </cv-row>

    <cv-row class="landing-title-row">
      <cv-column :lg="6" :md="8" :sm="4">
        <h1 class="landing-title">Drive Your Journey.</h1>
        <p class="landing-subtitle">
          Find the perfect rental vehicle - fast, reliable, and affordable.
        </p>
      </cv-column>
    </cv-row>

    <cv-row class="landing-tile-row">
      <cv-column class="landing-tile-container">
        <cv-tile
          v-for="(category, index) in vehicleStore.categories"
          :key="index"
          :light="true"
          kind="clickable"
          @click="handleCategorySearch(category)"
          class="landing-tile"
        >
          <h4 class="landing-tile-text">
            {{ category }}
          </h4>
        </cv-tile>
      </cv-column>
    </cv-row>

    <cv-row class="why-choose-us-row" id="why-choose-us">
      <cv-column :lg="7" :md="4" :sm="2">
        <h1>Why Choose Us?</h1>
        <div class="landing-selling-points-container">
          <h4><CheckMark16 class="landing-icon" />Free Cancellation</h4>

          <h4><Car class="landing-icon" />Wide Selection of Cars</h4>

          <h4><IBMSecurity class="landing-icon" />Secure Payments</h4>

          <h4><Time class="landing-icon" /> 24/7 Roadside Assistance</h4>
        </div>
      </cv-column>
      <cv-column :lg="5" :md="4" :sm="2" class="landing-car-logo-container">
        <img src="/src/assets/bmw-logo.png" class="landing-car-logo" />
        <img src="/src/assets/ford-logo.png" class="landing-car-logo" />
        <img src="/src/assets/mercedes-logo.jpeg" class="landing-car-logo" />
        <img src="/src/assets/porsche-logo.png" class="landing-car-logo" />
        <img src="/src/assets/vw-logo.png" class="landing-car-logo" />
        <img src="/src/assets/audi-logo.png" class="landing-car-logo" />
        <img src="/src/assets/honda-logo.png" class="landing-car-logo" />
        <img src="/src/assets/toyota-logo.png" class="landing-car-logo" />
      </cv-column>
    </cv-row>

    <!-- TODO replace with something else -->
    <img src="/src/assets/stay.png" style="width: 100%" />
  </cv-grid>
</template>

<style scoped>
.landing-hero-background {
  position: absolute;
  z-index: -1;
  width: 100%;
  height: 30rem;
  object-fit: cover;
  left: 0;
  top: 3rem;
}
.landing-hero-row {
  padding: 5rem;
  position: relative;
  margin-bottom: 4rem;
  max-height: 30rem;
}
.landing-title-row {
  margin-bottom: 4rem;
}
.landing-title {
  margin-bottom: 1rem;
  font-size: 60px;
}
.landing-subtitle {
  margin-bottom: 1rem;
  color: var(--cds-interactive);
}
.landing-form {
  margin-top: 5rem;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  background-color: var(--cds-background);
}
.landing-tile-row {
  margin-bottom: 4rem;
}
.landing-tile-container {
  display: flex;
  flex-wrap: wrap;
}
.landing-tile {
  flex: 0 0 25%;
  box-sizing: border-box;
  border: 1px solid var(--cds-border-subtle-01);
  height: 13.4rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.landing-tile-text {
  color: var(--cds-interactive);
  font-weight: 300;
}
.landing-selling-points-container {
  display: grid;
  padding-top: 2rem;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  width: 75%;
  gap: 2rem;
}
.landing-selling-points-container > {
  display: block;
}
.landing-icon {
  fill: var(--cds-interactive);
  height: 1.5rem;
  width: auto;
  margin: 0 1rem 0 0;
}
.landing-car-logo-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 2rem;
  align-items: center;
  justify-content: center;
  padding-top: 2rem;
}
.landing-car-logo {
  height: 3rem;
  width: auto;
}
.why-choose-us-row {
  margin-bottom: 4rem;
}

@media (max-width: 1055px) {
  .landing-tile-container,
  .landing-selling-points-container {
    grid-template-columns: 1fr;
  }
  .landing-title-row {
    margin-top: 10rem;
    text-align: center;
  }
}
</style>
