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
  analyticsStore.fetchRentalUtilisationByBranch(props.branch);
};

onMounted(fetchData);

watch(() => props.branch, fetchData);

const options = {
  title: "Rental Utilisation",
  resizable: true,
  gauge: {
    type: "full",
    alignment: "center",
  },
  height: "300px",
};
</script>

<template>
  <CcvGaugeChart
    :data="analyticsStore?.rentalUtilisationByBranch"
    :options="options"
  />
</template>
