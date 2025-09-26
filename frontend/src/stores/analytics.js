import { defineStore } from "pinia";
import api from "./axios";

export const useAnalyticsStore = defineStore("analytics", {
  state: () => ({
    fleetInsights: [],
    statusByBranch: [],
    categoryByBranch: [],
    rentalUtilisationByBranch: [],
    rentedByCategory: [],
    vehiclesWithIssues: [],
    error: null,
  }),
  actions: {
    async fetchFleetInsights() {
      try {
        const res = await api.get("/analytics/fleet", {});
        this.fleetInsights = res.data;
      } catch (err) {
        console.log("Failed to fetch fleet insights:", err);
      }
    },
    async fetchStatusByBranch(branch) {
      try {
        const res = await api.get("/analytics/status-by-branch", {
          params: { branch },
        });
        this.statusByBranch = res.data;
      } catch (err) {
        console.log("Failed to fetch status by branch:", err);
      }
    },
    async fetchCategoryByBranch(branch) {
      try {
        const res = await api.get("/analytics/category-by-branch", {
          params: { branch },
        });
        this.categoryByBranch = res.data;
      } catch (err) {
        console.log("Failed to fetch category by branch:", err);
      }
    },
    async fetchRentalUtilisationByBranch(branch) {
      try {
        const res = await api.get("/analytics/rental-utilisation-by-branch", {
          params: { branch },
        });
        this.rentalUtilisationByBranch = res.data;
      } catch (err) {
        console.log("Failed to fetch rental utilisation:", err);
      }
    },
    async fetchRentedByCategory(branch) {
      try {
        const res = await api.get("/analytics/rented-by-category", {
          params: { branch },
        });
        this.rentedByCategory = res.data;
      } catch (err) {
        console.log("Failed to fetch rented vehicles by category:", err);
      }
    },
    async fetchVehiclesWithIssues(branch) {
      try {
        const res = await api.get("/analytics/issues-percentage", {
          params: { branch },
        });
        this.vehiclesWithIssues = res.data;
      } catch (err) {
        console.log("Failed to fetch vehicles with issues:", err);
      }
    },
  },
});
