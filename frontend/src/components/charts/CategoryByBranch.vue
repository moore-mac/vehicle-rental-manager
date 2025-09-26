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
  analyticsStore.fetchCategoryByBranch(props.branch);
};

onMounted(fetchData);

watch(() => props.branch, fetchData);

const options = {
  title: "Vehicles by Category",
  resizable: true,
  legend: {
    position: "right",
    truncation: {
      type: "none",
    },
  },
  donut: {
    center: {
      label: "Vehicles",
    },
    alignment: "center",
  },
  height: "400px",
};
</script>

<template>
  <CcvDonutChart :data="analyticsStore?.categoryByBranch" :options />
</template>
