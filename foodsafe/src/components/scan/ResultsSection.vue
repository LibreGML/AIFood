<template>
  <div class="results-section">
    <v-card rounded="xl" class="mb-6">
      <v-card-title class="d-flex align-center">
        <v-icon :color="analysisResult.safe ? 'success' : 'error'" size="32" class="mr-2">
          {{ analysisResult.safe ? "mdi-shield-check" : "mdi-shield-alert" }}
        </v-icon>
        检测结果
      </v-card-title>
      <v-card-text>
        <div class="d-flex align-center mb-4">
          <v-chip :color="analysisResult.safe ? 'success' : 'error'" size="large" label>
            {{ analysisResult.safe ? "安全" : "存在风险" }}
          </v-chip>
          <div class="ml-auto text-h5 font-weight-bold">
            安全指数: {{ analysisResult.safetyScore }}%
          </div>
        </div>

        <div class="mb-6">
          <h3 class="text-h6 font-weight-bold mb-2">食品信息</h3>
          <v-list lines="two">
            <v-list-item v-for="(info, key) in analysisResult.foodInfo" :key="key">
              <v-list-item-title>{{ info.label }}</v-list-item-title>
              <v-list-item-subtitle>{{ info.value }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </div>

        <div v-if="!analysisResult.safe" class="mb-6">
          <h3 class="text-h6 font-weight-bold mb-2">风险提示</h3>
          <v-alert type="error" variant="tonal" rounded="lg">
            <div v-for="(risk, i) in analysisResult.risks" :key="i" class="mb-2">
              <strong>{{ risk.title }}:</strong> {{ risk.description }}
            </div>
          </v-alert>
        </div>

        <div>
          <h3 class="text-h6 font-weight-bold mb-2">建议</h3>
          <v-alert type="info" variant="tonal" rounded="lg">
            {{ analysisResult.recommendation }}
          </v-alert>
        </div>
      </v-card-text>
    </v-card>

    <v-btn block color="success" rounded="pill" @click="startNewScan">
      <v-icon start>mdi-plus</v-icon>
      新建检测
    </v-btn>
  </div>
</template>

<script setup>
const props = defineProps({
  analysisResult: Object,
});

const emit = defineEmits(["newScan"]);

const startNewScan = () => {
  emit("newScan");
};
</script>

<style scoped>
.results-section {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
