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
  analyticsStore.fetchRentedByCategory(props.branch);
};

onMounted(fetchData);

watch(() => props.branch, fetchData);

const options = {
  title: "Rented Vehicles by Category",
  resizable: true,
  pie: {
    alignment: "center",
  },
  height: "400px",
};
</script>

<template>
  <CcvPieChart :data="analyticsStore?.rentedByCategory" :options="options" />
</template>
