<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <div class="footer">
    <p>© 2024 Car Go. All rights reserved.</p>
    <div class="footer-links">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About Us</RouterLink>
      <RouterLink to="/contact">Contact</RouterLink>
      <RouterLink to="/privacy">Privacy Policy</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.footer {
  background-color: #161616;
  border-top: 1px solid var(--cds-border-subtle-01);
  padding: 1rem 2rem;
  text-align: center;
  position: relative;
  bottom: 0;
  width: 100%;
  height: 15rem;
}
</style>
