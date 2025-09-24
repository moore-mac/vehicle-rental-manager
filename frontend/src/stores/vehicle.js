import { defineStore } from "pinia";
import api from "./axios";

export const useVehicleStore = defineStore("vehicle", {
  state: () => ({
    vehicles: [],
    selectedVehicle: null,
    categories: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchAll() {
      this.loading = true;
      try {
        const res = await api.get("/cars/all");
        this.vehicles = res.data;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    async fetchAvailable() {
      this.loading = true;
      try {
        const res = await api.get("/cars/available");
        this.availableVehicles = res.data;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    async fetchVehiclesByBranch(branch = "") {
      try {
        const res = await api.get("/cars/fetch_by_branch", {
          params: { branch },
        });
        this.vehicles = res.data;
      } catch (error) {
        console.error("Failed to fetch vehicles:", error);
        this.vehiclesByBranch = {};
      }
    },

    async fetchByReg(reg) {
      const res = await api.get(`/cars/show?reg=${reg}`);
      this.selectedVehicle = res.data;
      return res.data;
    },

    async fetchByCategory(category) {
      const res = await api.get(`/cars/category?category=${category}`);
      this.vehicles = res.data;
      return res.data;
    },

    async fetchCategories() {
      const res = await api.get("/cars/category-list");
      this.categories = res.data;
      return res.data;
    },

    async rentVehicle(reg) {
      return await api.get(`/cars/rent?reg=${reg}`);
    },

    async returnVehicle(reg) {
      return await api.get(`/cars/return?reg=${reg}`);
    },

    async addVehicle(vehicleData) {
      return await api.get("/cars/add", { params: vehicleData });
    },

    async removeVehicle(reg) {
      return await api.get(`/cars/remove?reg=${reg}`);
    },

    async searchVehicles(params) {
      this.loading = true;
      try {
        const res = await api.get("/cars/search", { params });
        this.vehicles = res.data.results;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    async editVehicle(reg, updates) {
      return await api.get("/cars/edit", { params: { reg, ...updates } });
    },

    async bulkAdd(vehicles) {
      return await api.post("/cars/bulk-add", vehicles);
    },

    async batchEdit(updates) {
      return await api.post("/cars/batch-edit", updates);
    },
  },
});
