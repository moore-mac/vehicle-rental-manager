<script setup>
import { RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
import PageFooter from "./components/PageFooter.vue";
</script>

<template>
  <div>
    <NavBar />

    <cv-content style="padding-top: 5rem">
      <RouterView />
    </cv-content>

    <PageFooter />
  </div>
</template>

<style>
body {
  background-color: var(--cds-background) !important;
}
.nav-bar {
  border-color: var(--cds-border-subtle) !important;
}
.nav-bar-logo {
  filter: sepia(100%) hue-rotate(175deg) saturate(1050%);
  height: 2.5rem;
}
</style>
