<template>
  <div class="home-page">
    <AppBar />
    <IndexHeroSection />
    <IndexFeaturesSection />
    <IndexStatsSection />
    <IndexHowItWorks />
  </div>
</template>

<script setup>
import AppBar from "@/components/AppBar.vue";
import IndexFeaturesSection from "@/components/index/FeaturesSection.vue";
import IndexHeroSection from "@/components/index/HeroSection.vue";
import IndexHowItWorks from "@/components/index/HowItWorks.vue";
import IndexStatsSection from "@/components/index/StatsSection.vue";
</script>

<style scoped></style>
