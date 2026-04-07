<template>
  <section class="features-section py-8 py-md-16">
    <v-container>
      <h2 class="text-h5 text-md-h3 font-weight-bold text-center mb-2">为什么选择我们</h2>
      <p class="text-subtitle-2 text-medium-emphasis text-center mb-8 mb-md-10">
        先进的技术和专业的服务保障您的食品安全
      </p>

      <v-row>
        <v-col cols="12" sm="4" v-for="(feature, i) in features" :key="i">
          <v-card :color="feature.color" class="h-100" variant="outlined" rounded="xl">
            <v-card-text class="pa-4 pa-md-6 text-center">
              <v-icon size="48" class="mb-3 mb-md-4">{{ feature.icon }}</v-icon>
              <h3 class="text-h6 text-md-h5 font-weight-bold mb-2">
                {{ feature.title }}
              </h3>
              <p class="text-body-2 text-caption text-md-body2">
                {{ feature.description }}
              </p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup>
const features = [
  {
    icon: "mdi-shield-check",
    title: "权威认证",
    description: "通过国家权威机构认证，检测结果准确可靠",
    color: "success-lighten-5",
  },
  {
    icon: "mdi-clock-fast",
    title: "快速检测",
    description: "仅需几秒钟即可完成检测，无需等待",
    color: "info-lighten-5",
  },
  {
    icon: "mdi-database",
    title: "大数据支持",
    description: "基于海量食品数据库，覆盖常见食品种类",
    color: "warning-lighten-5",
  },
];
</script>

<style scoped>
.features-section {
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
