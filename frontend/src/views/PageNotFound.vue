<script>
export default {
  name: "NotFoundPage",
};
</script>

<template>
  <div class="page-404">
    <h1 class="error-code">404</h1>
    <p class="message">Looks like you took a wrong turn on the road.</p>
  </div>
</template>

<style scoped>
.page-404 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 13rem);
  text-align: center;
  color: #333;
}
.error-code {
  font-size: 8rem;
  font-weight: bold;
  margin: 0;
}
.message {
  font-size: 1.5rem;
  margin-top: 1rem;
  color: #555;
}
</style>
