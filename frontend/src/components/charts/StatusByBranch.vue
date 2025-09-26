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
  analyticsStore.fetchStatusByBranch(props.branch);
};

onMounted(fetchData);

watch(() => props.branch, fetchData);

const options = {
  title: "Vehicles by Status",
  axes: {
    left: {
      title: "Number of Vehicles",
      mapsTo: "value",
    },
    bottom: {
      title: "Status",
      mapsTo: "group",
      scaleType: "labels",
    },
  },
  height: "400px",
};
</script>

<template>
  <CcvSimpleBarChart :data="analyticsStore.statusByBranch" :options />
</template>
