<template>
  <section class="how-it-works py-10 py-md-16">
    <v-container>
      <h2 class="text-h4 text-md-h3 font-weight-bold text-center mb-2">如何使用</h2>
      <p class="text-subtitle-1 text-medium-emphasis text-center mb-10">
        简单三步，快速检测食品安全
      </p>

      <v-row>
        <v-col cols="12" md="4" v-for="(step, i) in steps" :key="i">
          <v-card class="h-100" variant="text">
            <v-card-text class="pa-6 text-center">
              <v-avatar :color="step.color" size="64" class="mb-4">
                <span class="text-h4 font-weight-bold">{{ i + 1 }}</span>
              </v-avatar>
              <h3 class="text-h5 font-weight-bold mb-2">{{ step.title }}</h3>
              <p class="text-body-2">{{ step.description }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup>
const steps = [
  {
    title: "拍照上传",
    description: "使用手机拍摄食品包装或实物照片",
    color: "success",
  },
  {
    title: "AI识别",
    description: "系统自动识别食品信息并分析成分",
    color: "info",
  },
  {
    title: "获取结果",
    description: "查看详细检测报告和安全建议",
    color: "warning",
  },
];
</script>

<style scoped>
.how-it-works {
  background-color: white;
}

:deep(.v-card) {
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
}
</style>