<script setup></script>

<template>
  <div class="footer">
    <p>Home</p>
    <p>About Us</p>
    <p>Contact</p>
    <p>Privacy Policy</p>
  </div>
</template>

<style scoped>
.footer {
  background-color: #161616;
  border-top: 1px solid var(--cds-border-subtle-01);
  padding: 1rem;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  position: relative;
  width: 100%;
  min-height: 15rem;
  margin-top: 4rem;
}
.footer p {
  text-decoration: none;
  cursor: pointer;
  color: var(--cds-text-inverse);
}
</style>
