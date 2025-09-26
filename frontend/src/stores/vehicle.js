import { defineStore } from "pinia";
import api from "./axios";

export const useVehicleStore = defineStore("vehicle", {
  state: () => ({
    vehicles: [],
    globalSearchResults: [],
    selectedVehicle: null,
    categories: [],
    branches: [],
    statuses: [],
    statusColourMap: {
      AVAILABLE: "green",
      RENTED: "red",
      SERVICEREQ: "red",
      DAMAGED: "red",
    },
    statusLabelMap: {
      AVAILABLE: "Available",
      RENTED: "Rented",
      SERVICEREQ: "Service Required",
      DAMAGED: "Damaged",
    },
    filters: {},
  }),
  getters: {
    branchOptions: (state) =>
      state.branches.map((branch, index) => ({
        name: `branch-${index + 1}`,
        label: branch,
        value: branch,
      })),

    categoryOptions: (state) =>
      state.categories.map((category, index) => ({
        name: `category-${index + 1}`,
        label: category,
        value: category,
      })),

    statusOptions: (state) =>
      state.statuses.map((status, index) => ({
        name: `status-${index + 1}`,
        label: state.statusLabelMap[status],
        value: status,
      })),
  },
  actions: {
    async fetchAll() {
      try {
        const res = await api.get("/cars/all");
        this.vehicles = res.data;
      } catch (err) {
        console.error("Failed to fetch all vehicles:", err);
      }
    },

    async fetchAvailable() {
      try {
        const res = await api.get("/cars/available");
        this.availableVehicles = res.data;
      } catch (err) {
        console.error("Failed to fetch available vehicles:", err);
      }
    },

    async fetchVehiclesByBranch(branch = "") {
      try {
        const res = await api.get("/cars/fetch_by_branch", {
          params: { branch },
        });
        this.vehicles = res.data;
      } catch (err) {
        console.error("Failed to fetch vehicles by branch:", err);
      }
    },

    async fetchByReg(reg) {
      try {
        const res = await api.get(`/cars/show?reg=${reg}`);
        this.selectedVehicle = res.data;
        return res.data;
      } catch (err) {
        console.error("Failed to fetch vehicle by reg:", err);
      }
    },

    async fetchByCategory(category) {
      try {
        const res = await api.get(`/cars/category?category=${category}`);
        this.vehicles = res.data;
        return res.data;
      } catch (err) {
        console.error("Failed to fetch vehicles by category:", err);
      }
    },

    async fetchCategories() {
      try {
        const res = await api.get("/cars/category-list");
        this.categories = res.data;
        return res.data;
      } catch (err) {
        console.error("Failed to fetch categories:", err);
      }
    },

    async fetchBranches() {
      try {
        const res = await api.get("/cars/branch-list");
        this.branches = res.data;
      } catch (err) {
        console.error("Failed to fetch branches:", err);
      }
    },

    async fetchStatuses() {
      try {
        const res = await api.get("/cars/status-list");
        this.statuses = res.data;
      } catch (err) {
        console.error("Failed to fetch statuses:", err);
      }
    },

    async rentVehicle(reg) {
      try {
        return await api.put(`/cars/rent?reg=${reg}`);
      } catch (err) {
        console.error("Failed to rent vehicle:", err);
      }
    },

    async returnVehicle(reg) {
      try {
        return await api.put(`/cars/return?reg=${reg}`);
      } catch (err) {
        console.error("Failed to return vehicle:", err);
      }
    },

    async addVehicle(vehicleData) {
      try {
        // using csv, so convert all values to strings
        const payload = Object.fromEntries(
          Object.entries(vehicleData).map(([key, value]) => [
            key,
            String(value ?? ""),
          ])
        );

        const res = await api.post("/cars/add", payload);
        const newVehicle = res.data.vehicle;

        this.vehicles.push(newVehicle);

        return newVehicle;
      } catch (err) {
        console.error("Failed to add vehicle:", err);
      }
    },

    async removeVehicle(id) {
      try {
        const res = await api.post(`/cars/remove?id=${id}`);
        this.vehicles = this.vehicles.filter((v) => v.id !== id);
        return res.data;
      } catch (err) {
        console.error("Failed to remove vehicle:", err);
      }
    },

    async batchRemoveVehicles(arrayOfIds) {
      try {
        const res = await api.post("/cars/remove-batch", { ids: arrayOfIds });
        this.vehicles = this.vehicles.filter((v) => !arrayOfIds.includes(v.id));
        return res.data;
      } catch (err) {
        console.error("Failed to batch remove vehicles:", err);
      }
    },

    async searchVehicles(params) {
      try {
        const res = await api.get("/cars/search", { params });
        this.vehicles = res.data.results;
      } catch (err) {
        console.error("Failed to search vehicles:", err);
      }
    },

    async globalSearch(params) {
      try {
        const res = await api.get("/cars/search", { params });
        this.globalSearchResults = res.data.results;
      } catch (err) {
        console.error("Failed to run global search:", err);
      }
    },

    async editVehicle(reg, updates) {
      try {
        return await api.put("/cars/edit", { params: { reg, ...updates } });
      } catch (err) {
        console.error("Failed to edit vehicle:", err);
      }
    },

    async bulkAdd(vehicles) {
      try {
        return await api.post("/cars/bulk-add", vehicles);
      } catch (err) {
        console.error("Failed to bulk add vehicles:", err);
      }
    },

    async batchEdit(updates) {
      try {
        return await api.put("/cars/batch-edit", updates);
      } catch (err) {
        console.error("Failed to batch edit vehicles:", err);
      }
    },
  },
});
