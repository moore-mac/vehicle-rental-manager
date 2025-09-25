<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useVehicleStore } from "@/stores/vehicle";

const vehicleStore = useVehicleStore();
const isLoading = ref(false);
const showDropdown = ref(false);
const searchWrapper = ref(null);

function debounce(fn, delay = 400) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

async function doSearch(query) {
  if (!query) {
    vehicleStore.globalSearchResults = [];
    return;
  }

  try {
    isLoading.value = true;
    await vehicleStore.globalSearch({ query, limit: 5 });
  } catch (err) {
    console.error("Search error:", err);
    vehicleStore.globalSearchResults = [];
  } finally {
    isLoading.value = false;
  }
}

const onSearch = debounce(doSearch, 400);

function handleClickOutside(event) {
  if (searchWrapper.value && !searchWrapper.value.contains(event.target)) {
    showDropdown.value = false;
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>

<template>
  <div class="nav-bar">
    <img
      src="/src/assets/car-go-logo.png"
      alt="car go logo"
      class="nav-bar-logo"
      @click="$router.push('/')"
    />

    <!-- Search bar -->
    <div class="nav-search-wrapper" ref="searchWrapper">
      <cv-search
        label="search"
        placeholder="Make, Model, Location..."
        size="xl"
        :light="true"
        :expandable="false"
        @input="onSearch"
        @focus="showDropdown = true"
      />
      <!-- Dropdown results -->
      <ul
        v-if="showDropdown && vehicleStore.globalSearchResults.length"
        class="search-results"
      >
        <li
          v-for="vehicle in vehicleStore.globalSearchResults"
          :key="vehicle.id"
          class="search-result-item"
          @click="
            $router.push({
              path: '/vehicles',
              query: { vrm: vehicle.vrm },
            });
            showDropdown = false;
          "
        >
          <strong>{{ vehicle.make }} {{ vehicle.model }}</strong>
          — {{ vehicle.vrm }} ({{ vehicle.branch }})
        </li>
      </ul>
    </div>

    <div class="nav-bar-menu">
      <div class="nav-bar-menu-item" @click="$router.push('/my-fleet')">
        My Fleet
      </div>
      <div class="nav-bar-menu-item" @click="$router.push('/analytics')">
        Analytics
      </div>
      <div class="nav-bar-menu-item disabled" @click="$router.push('/')">
        My Bookings
      </div>
      <div class="nav-bar-menu-item disabled" @click="$router.push('/')">
        Settings
      </div>
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
  z-index: 9999;
  border-bottom: 1px solid var(--cds-border-subtle-01);
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
  font-family: "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
}
.nav-bar-menu-item {
  width: fit-content;
  padding: 1rem 2rem 1rem 2rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.nav-bar-menu-item:hover {
  background-color: lightgray;
}
.nav-bar-menu-item.disabled {
  color: gray;
  cursor: not-allowed;
}

/* Search wrapper and results */
.nav-search-wrapper {
  position: relative;
  flex: 1;
  max-width: 400px;
}
.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--cds-border-subtle-01);
  border-top: none;
  list-style: none;
  padding: 0;
  margin: 0;
  z-index: 10000;
  max-height: 15rem;
  overflow-y: auto;
}
.search-result-item {
  padding: 1rem 1rem;
  border-bottom: 1px solid var(--cds-border-subtle-01);
  cursor: pointer;
  font-size: 0.875rem;
}
.search-result-item:last-of-type {
  border: none;
}
.search-result-item:hover {
  background-color: #f4f4f4;
}
</style>
