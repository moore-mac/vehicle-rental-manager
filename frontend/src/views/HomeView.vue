<script setup></script>

<template>
  <cv-grid>
    <cv-row>
      <cv-column :lg="8" :md="8" :sm="4">
        <cv-row class="landing-hero">
          <cv-column :lg="6" :md="4" :sm="4">
            <h1 class="landing-title">Drive Your Journey</h1>
            <p class="landing-subtitle">
              Find the perfect rental vehicle - fast, reliable, and affordable.
            </p>
          </cv-column>

          <cv-column :lg="6" :md="4" :sm="4">
            <!-- TODO add search function -->

            <!-- TODO add submit and learn more functions -->
          </cv-column>
        </cv-row>
        <div class="landing-car-graphic-container">
          <img
            src="../assets/landing-bmw.png"
            alt="bmw pic"
            class="landing-car-graphic"
          />
        </div>
      </cv-column>

      <cv-column :lg="4" :md="8" :sm="4">
        <cv-form
          @submit.prevent="() => {}"
          style="
            display: flex;
            flex-direction: column;
            gap: 2rem;
            padding: 2rem;
          "
        >
          <h3>Find a Ride</h3>
          <cv-combo-box
            title="Collect From"
            label="City"
            :options="[
              { name: 'something-1', label: 'London', value: 'val-1' },
            ]"
            value="21"
            :is-light="false"
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
              :light="false"
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
      </cv-column>
    </cv-row>

    <img src="/src/assets/landing-bmw.png" alt="" style="width: 40%" />
    <img
      src="/src/assets/tiles.png"
      alt=""
      style="
        width: 50%;
        float: right;
        border-bottom: 1px solid var(--cds-border-subtle-01);
      "
    />
    <!-- <img src="/src/assets/c-test.png" alt="" style="width: 100%" /> -->
    <img src="/src/assets/stay.png" alt="" style="width: 100%" />
  </cv-grid>
</template>

<style scoped>
.landing-hero {
  /* background-color: var(--cds-layer-01); */
  /* border: 1px solid var(--cds-border-subtle-01); */
  padding: 1rem 2rem 5rem 3rem;
  /* box-shadow: 0 4px 6px -2px rgba(0, 0, 0, 0.2); */
}
.landing-title {
  margin-bottom: 1rem;
  font-size: 60px;
}
.landing-subtitle {
  margin-bottom: 1rem;
  color: var(--cds-interactive);
}
.landing-car-graphic-container {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
}
.landing-car-graphic {
  width: auto;
  height: 50%;
  filter: blur(0.5px);
  display: none;
}
</style>
