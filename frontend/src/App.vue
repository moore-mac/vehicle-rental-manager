<script setup>
import { onMounted, onBeforeUnmount } from "vue";
import { RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
import PageFooter from "./components/PageFooter.vue";

let lastScroll = 0;
let offset = 0;
let navbar = null;
let navbarHeight = 0;

onMounted(() => {
  navbar = document.getElementById("navbar");
  if (!navbar) return;

  navbarHeight = navbar.offsetHeight;

  const handleScroll = () => {
    const currentScroll = window.pageYOffset;
    const delta = currentScroll - lastScroll;

    offset += delta;
    offset = Math.max(0, Math.min(offset, navbarHeight));
    navbar.style.transform = `translateY(-${offset}px)`;

    lastScroll = currentScroll;
  };

  window.addEventListener("scroll", handleScroll);

  onBeforeUnmount(() => {
    window.removeEventListener("scroll", handleScroll);
  });
});
</script>

<template>
  <NavBar id="navbar" />

  <cv-content style="padding-top: 6rem">
    <RouterView />
  </cv-content>

  <PageFooter />
</template>

<style>
body {
  background-color: var(--cds-background) !important;
}
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.bx--content {
  flex: 1;
}
.nav-bar {
  border-color: var(--cds-border-subtle-01) !important;
}
.nav-bar-logo {
  filter: sepia(100%) hue-rotate(175deg) saturate(1050%);
  height: 2.5rem;
}
.bx--search-input {
  border: none !important;
}
.bx--search {
  padding-bottom: 1px !important;
}
.bx--breadcrumb-item {
  color: #0f62fe;
  cursor: pointer;
}
</style>
