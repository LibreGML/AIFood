<template>
  <v-app id="app">
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
</script>

<style lang="scss">
#app {
  background-color: #f8fafc;
  min-height: 100vh;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.v-card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
    transition: box-shadow 0.3s ease;
  }
}

.v-btn {
  text-transform: none !important;
  letter-spacing: normal !important;
}

.text-h1,
.text-h2,
.text-h3,
.text-h4,
.text-h5,
.text-h6 {
  font-weight: 700 !important;
  line-height: 1.3 !important;
}

@media (max-width: 600px) {
  .container {
    padding: 12px !important;
  }
}
</style>
