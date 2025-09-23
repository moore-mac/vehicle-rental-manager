import { defineStore } from "pinia";
import api from "./axios";

export const useBranchStore = defineStore("branch", {
  state: () => ({
    branches: [],
  }),

  actions: {
    async fetchBranches() {
      const res = await api.get("/cars/branch-list");
      this.branches = res.data;
    },
  },
});
