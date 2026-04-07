<template>
  <section class="stats-section py-6 py-md-16">
    <v-container>
      <v-row>
        <v-col cols="6" md="3" v-for="(stat, i) in stats" :key="i">
          <div class="text-center">
            <div class="text-h5 text-md-h2 font-weight-bold text-success mb-1 mb-md-2">
              {{ stat.value }}
            </div>
            <div class="text-caption text-md-subtitle-2 text-medium-emphasis">
              {{ stat.label }}
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup>
const stats = [
  { value: "10万+", label: "检测次数" },
  { value: "99.8%", label: "准确率" },
  { value: "5000+", label: "食品种类" },
  { value: "24小时", label: "服务时间" },
];
</script>

<style scoped>
.stats-section {
  background-color: #f1f8e9;
}
</style>
