<script setup>
import { useAnalyticsStore } from "@/stores/analytics";
import { computed, onMounted } from "vue";

const analyticsStore = useAnalyticsStore();

const fleetInsights = computed(() => analyticsStore.fleetInsights);

onMounted(analyticsStore.fetchFleetInsights);

// Utility formatters
function formatKey(key) {
  return key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
}
function formatValue(key, value) {
  if (key.includes("rate")) {
    return value.toFixed(2) + (key.includes("day") ? " £/day" : "%");
  }
  return value;
}
</script>

<template>
  <div class="dashboard" v-if="Object.keys(fleetInsights).length > 0">
    <div class="summary">
      <div
        class="metric"
        v-for="(value, key) in fleetInsights.summary"
        :key="key"
      >
        <h3>{{ formatKey(key) }}</h3>
        <p>{{ formatValue(key, value) }}</p>
      </div>
    </div>

    <cv-row>
      <cv-column class="branch-performance">
        <p class="title">Branch Performance</p>
        <br />
        <table>
          <thead>
            <tr>
              <th>Branch</th>
              <th>Available</th>
              <th>Rented</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(data, branch) in fleetInsights.branch_performance"
              :key="branch"
            >
              <td>{{ branch }}</td>
              <td>{{ data.available }}</td>
              <td>{{ data.rented }}</td>
              <td>{{ data.total }}</td>
            </tr>
          </tbody>
        </table>
      </cv-column>

      <cv-column class="fleet-composition">
        <CcvSimpleBarChart
          :data="fleetInsights.fleet_composition.by_category"
          :options="{
            title: 'Fleet Composition by Category',
            axes: {
              left: {
                title: 'Number of Vehicles',
                mapsTo: 'value',
              },
              bottom: {
                title: 'Category',
                mapsTo: 'group',
                scaleType: 'labels',
              },
            },
            height: '300px',
          }"
        />
      </cv-column>
    </cv-row>

    <CcvTreemapChart
      :data="fleetInsights.fleet_composition.by_make"
      :options="{
        title: 'Fleet Composition by Make',
        height: '800px',
      }"
    />
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  position: relative;
  width: 100%;
  padding-top: 2rem;
}

.summary {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 2rem;
  margin-bottom: 3rem;
}
.metric {
  text-align: center;
}
.metric h3 {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}
.metric p {
  font-size: 2rem;
}
.branch-performance {
  padding-right: 2rem;
}
.branch-performance .title {
  color: var(--cds-text-primary);
  font-size: 16px;
  font-family: var(--cds-charts-font-family);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 8px 15px 10px 0;
}
.branch-performance table {
  width: 100%;
  border-collapse: collapse;
}
.branch-performance th,
.branch-performance td {
  padding: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
}
.branch-performance th {
  background: #f3f4f6;
  font-weight: 600;
}
.fleet-composition {
  padding-left: 2rem;
}
</style>
