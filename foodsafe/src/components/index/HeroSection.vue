<template>
  <section class="hero-section">
    <v-container class="py-6 py-md-16">
      <v-row align="center" justify="center">
        <v-col cols="12" md="6">
          <h1 class="text-h4 text-md-h1 font-weight-bold mb-3 mb-md-4">
            食品安全检测平台
          </h1>
          <p class="text-subtitle-1 text-md-h5 mb-6">
            利用AI技术快速检测食品质量与安全，保障您和家人的饮食健康
          </p>
          <div class="d-flex flex-column flex-sm-row ga-3 ga-md-4">
            <v-btn
              color="success"
              size="large"
              rounded="pill"
              @click="goToScan"
              class="text-capitalize px-6 px-md-8 align-self-center align-self-sm-auto"
              :block="$vuetify.display.xs"
              :class="{ 'mb-3': $vuetify.display.xs }"
            >
              <v-icon start>mdi-camera</v-icon>
              立即检测
            </v-btn>
            <v-btn
              variant="outlined"
              size="large"
              rounded="pill"
              @click="goToKnowledge"
              class="text-capitalize px-6 px-md-8 align-self-center align-self-sm-auto"
              :block="$vuetify.display.xs"
              :class="{ 'mb-3': $vuetify.display.xs }"
            >
              <v-icon start>mdi-book-open</v-icon>
              知识库
            </v-btn>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="d-none d-md-block">
          <v-img aspect-ratio="1" class="rounded-xl"></v-img>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const goToScan = () => {
  router.push("/scan");
};

const goToKnowledge = () => {
  router.push("/knowledge");
};
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #e3f2fd 0%, #f1f8e9 100%);
  min-height: 70vh;
  display: flex;
  align-items: center;
}
</style>
