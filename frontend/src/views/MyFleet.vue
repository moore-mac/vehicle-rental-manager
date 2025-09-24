<script setup></script>

<template>
  <cv-grid>
    <cv-row>
      <cv-column>
        <cv-breadcrumb :no-trailing-slash="false">
          <cv-breadcrumb-item @click="$router.push('/')">
            Home
          </cv-breadcrumb-item>
        </cv-breadcrumb>
        <!-- TODO -->
        <h1>My Fleet</h1>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<style scoped></style>
