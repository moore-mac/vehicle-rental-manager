<script setup>
import { RouterLink } from "vue-router";
import { ref } from "vue";

const searchInput = ref("");
</script>

<template>
  <div class="nav-bar">
    <!-- TODO routing -->
    <img
      src="/src/assets/car-go-logo.png"
      alt="car go logo"
      class="nav-bar-logo"
      @click="$router.push('/')"
    /><cv-search
      v-model="searchInput"
      label="search"
      placeholder="Make, Model, Location..."
      size="xl"
      :light="true"
      :expandable="false"
      @input="searchInput = input"
    >
    </cv-search>
    <div class="nav-bar-menu">
      <div class="nav-bar-menu-item" @click="$router.push('/my-fleet')">
        My Fleet
      </div>
      <div class="nav-bar-menu-item" @click="$router.push('/analytics')">
        Analytics
      </div>
      <div class="nav-bar-menu-item" @click="$router.push('/')">
        My Bookings
      </div>
      <div class="nav-bar-menu-item" @click="$router.push('/')">Settings</div>
    </div>
  </div>
</template>

<style scoped>
.nav-bar {
  height: 3rem;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: var(--cds-background);
  position: fixed;
  /* border-bottom: 1px solid var(--cds-border-subtle-01); */
}
.nav-bar-logo {
  height: 2.5rem;
  padding: 0 !important;
  margin: 0 2rem;
  cursor: pointer;
  filter: sepia(100%) hue-rotate(175deg) saturate(1050%);
  transition: filter 0.3s ease;
}
.nav-bar-logo:hover {
  filter: sepia(100%) hue-rotate(175deg) saturate(1050%) brightness(75%);
}
.nav-bar-menu {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  font-family: "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
  /* padding-right: 2rem; */
}
.nav-bar-menu-item {
  width: fit-content;
  padding: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.nav-bar-menu-item:hover {
  background-color: lightgray;
}
</style>
