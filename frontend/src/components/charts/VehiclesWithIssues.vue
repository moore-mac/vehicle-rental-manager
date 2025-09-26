<script setup>
import { onMounted, watch } from "vue";
import { useAnalyticsStore } from "@/stores/analytics";

const props = defineProps({
  branch: {
    type: String,
    required: false,
    default: "",
  },
});

const analyticsStore = useAnalyticsStore();

const fetchData = () => {
  analyticsStore.fetchVehiclesWithIssues(props.branch);
};

onMounted(fetchData);

watch(() => props.branch, fetchData);

const options = {
  title: "Vehicles with Issues",
  meter: {
    status: {
      ranges: [
        {
          range: [0, 50],
          status: "success",
        },
        {
          range: [50, 60],
          status: "warning",
        },
        {
          range: [60, 100],
          status: "danger",
        },
      ],
    },
  },
  height: "300px",
};
</script>

<template>
  <div v-if="analyticsStore.vehiclesWithIssues.length > 0">
    <CcvMeterChart
      :data="analyticsStore.vehiclesWithIssues"
      :options="options"
    />
  </div>
</template>
