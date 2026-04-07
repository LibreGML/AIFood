<template>
  <div class="d-flex align-center justify-space-between mb-8">
    <div>
      <h1 class="text-h4 text-md-h3 font-weight-bold mb-2">检测历史</h1>
      <p class="text-subtitle-1 text-medium-emphasis">
        查看您之前的食品安全检测记录和报告
      </p>
    </div>
    <v-btn
      color="success"
      rounded="pill"
      @click="$router.push('/scan')"
      class="d-none d-sm-flex"
    >
      <v-icon start>mdi-plus</v-icon>
      新建检测
    </v-btn>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>
