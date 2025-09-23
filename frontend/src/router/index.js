import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SearchResults from "@/views/SearchResults.vue";
import PageNotFound from "../views/PageNotFound.vue";
import VehicleDetails from "@/views/VehicleDetails.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/results",
      name: "results",
      component: SearchResults,
    },
    {
      path: "/vehicle",
      name: "vehicle-details",
      component: VehicleDetails,
    },
    {
      path: "/:pathMatch(.*)*", // catch-all route
      name: "NotFound",
      component: PageNotFound,
    },
  ],
});

export default router;
