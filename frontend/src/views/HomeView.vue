<script setup></script>

<template>
  <cv-grid>
    <cv-row class="landing-hero">
      <cv-column :lg="9" :md="4" :sm="2">
        <h1 class="landing-title">Drive Your Journey</h1>
        <p class="landing-subtitle">
          Find the perfect rental vehicle - fast, reliable, and affordable.
        </p>
      </cv-column>

      <cv-column :lg="3" :md="4" :sm="2">
        <!-- TODO add search function -->
        <cv-form
          @submit.prevent="() => {}"
          style="display: flex; flex-direction: column; gap: 1rem"
        >
          <cv-combo-box
            title="Collect From"
            label="City"
            :options="[
              { name: 'something-1', label: 'London', value: 'val-1' },
            ]"
            value="21"
            :is-light="true"
          ></cv-combo-box>

          <!-- TODO add vmodel -->
          <div style="display: flex; flex-direction: row; gap: 1rem">
            <cv-date-picker
              dateLabel="Date From"
              dateEndLabel="Date To"
              :cal-options="{ dateFormat: 'd/m/Y' }"
              placeholder="dd-mm-yyyy"
              invalidMessage=""
              kind="range"
              :light="true"
            >
            </cv-date-picker>
          </div>
          <cv-checkbox
            label="Driver aged over 25"
            @change="() => {}"
            :inline="true"
          ></cv-checkbox>

          <div>
            <cv-button kind="primary">Submit</cv-button>
            <cv-button kind="secondary">Learn More</cv-button>
          </div>
        </cv-form>
        <!-- TODO add submit and learn more functions -->
      </cv-column>
    </cv-row>
    <div class="landing-car-graphic-container">
      <img src="../assets/landing-bmw.png" alt="" />
    </div>
  </cv-grid>
</template>

<style scoped>
.landing-hero {
  background-color: var(--cds-layer-01);
  padding: 2rem;
  box-shadow: 0 6px 6px -2px rgba(0, 0, 0, 0.3);
}
.landing-title {
  margin-bottom: 1rem;
}
.landing-subtitle {
  margin-bottom: 1rem;
}
.landing-car-graphic-container {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
}
/* filter: sepia(100%) hue-rotate(190deg) saturate(500%); */
</style>
