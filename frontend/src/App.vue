<script setup>
import { RouterView } from "vue-router";
</script>

<template>
  <div>
    <cv-header class="nav-bar">
      <!-- TODO routing -->
      <!-- <cv-header-name
        href="javascript:void(0)"
        prefix="CAR"
        style="font-size: large"
      >
        GO
      </cv-header-name> -->
      <img
        src="/src/assets/car-go-logo.png"
        alt=""
        style="
          filter: sepia(100%) hue-rotate(175deg) saturate(1050%);
          height: 2.5rem;
        "
      />
      <cv-header-nav aria-label="Carbon nav">
        <cv-header-menu-item href="javascript:void(0)">
          My Fleet
        </cv-header-menu-item>
        <cv-header-menu-item href="javascript:void(0)">
          Analytics
        </cv-header-menu-item>
        <cv-header-menu-item href="javascript:void(0)">
          My Fleet
        </cv-header-menu-item>
      </cv-header-nav>
    </cv-header>

    <cv-content>
      <RouterView />
    </cv-content>
  </div>
</template>

<style>
body {
  background-color: var(--cds-background) !important;
}
.nav-bar {
  border-color: var(--cds-border-subtle) !important;
}
</style>
