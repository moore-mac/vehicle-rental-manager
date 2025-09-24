import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/views/HomeView.vue"),
    },
    {
      path: "/results",
      name: "results",
      component: () => import("@/views/SearchResults.vue"),
    },
    {
      path: "/vehicle",
      name: "vehicle-details",
      component: () => import("@/views/VehicleDetails.vue"),
    },
    {
      path: "/my-fleet",
      name: "my-fleet",
      component: () => import("@/views/MyFleet.vue"),
    },
    {
      path: "/analytics",
      name: "analytics",
      component: () => import("@/views/AnalyticsView.vue"),
    },
    {
      path: "/:pathMatch(.*)*", // catch-all route
      name: "NotFound",
      component: () => import("@/views/PageNotFound.vue"),
    },
  ],
});

export default router;
