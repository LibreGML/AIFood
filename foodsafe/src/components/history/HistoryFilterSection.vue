import { computed } from "vue";

<template>
  <v-card rounded="xl" class="mb-6 sticky-filters">
    <v-card-title class="text-h6 font-weight-bold d-flex align-center">
      <v-icon start>mdi-filter</v-icon>
      筛选条件
    </v-card-title>
    <v-card-text>
      <v-select
        v-model="localFilterStatus"
        :items="statusOptions"
        label="检测结果"
        variant="outlined"
        rounded="xl"
        hide-details
        class="mb-4"
      ></v-select>

      <v-select
        v-model="localFilterDate"
        :items="dateOptions"
        label="检测时间"
        variant="outlined"
        rounded="xl"
        hide-details
        class="mb-4"
      ></v-select>

      <v-text-field
        v-model="localSearchQuery"
        label="搜索食品"
        placeholder="输入食品名称"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        rounded="xl"
        hide-details
        clearable
      ></v-text-field>
    </v-card-text>

    <v-card-actions>
      <v-btn block color="success" rounded="pill" @click="applyFilters"> 应用筛选 </v-btn>
    </v-card-actions>
  </v-card>

  <v-card rounded="xl" class="sticky-stats">
    <v-card-title class="text-h6 font-weight-bold d-flex align-center">
      <v-icon start>mdi-chart-bar</v-icon>
      统计信息
    </v-card-title>
    <v-card-text>
      <div class="d-flex align-center mb-4">
        <v-avatar size="48" color="success" class="mr-3">
          <v-icon color="white">mdi-shield-check</v-icon>
        </v-avatar>
        <div>
          <div class="text-h6 font-weight-bold">{{ stats.safe }}</div>
          <div class="text-caption text-medium-emphasis">安全食品</div>
        </div>
      </div>

      <div class="d-flex align-center mb-4">
        <v-avatar size="48" color="error" class="mr-3">
          <v-icon color="white">mdi-shield-alert</v-icon>
        </v-avatar>
        <div>
          <div class="text-h6 font-weight-bold">{{ stats.unsafe }}</div>
          <div class="text-caption text-medium-emphasis">风险食品</div>
        </div>
      </div>

      <div class="d-flex align-center">
        <v-avatar size="48" color="info" class="mr-3">
          <v-icon color="white">mdi-history</v-icon>
        </v-avatar>
        <div>
          <div class="text-h6 font-weight-bold">{{ stats.total }}</div>
          <div class="text-caption text-medium-emphasis">总检测数</div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed, defineEmits, defineProps } from "vue";

const props = defineProps({
  stats: Object,
  filterStatus: String,
  filterDate: String,
  searchQuery: String,
});

const emit = defineEmits([
  "update:filterStatus",
  "update:filterDate",
  "update:searchQuery",
  "applyFilters",
]);

const localFilterStatus = computed({
  get: () => props.filterStatus,
  set: (value) => emit("update:filterStatus", value),
});

const localFilterDate = computed({
  get: () => props.filterDate,
  set: (value) => emit("update:filterDate", value),
});

const localSearchQuery = computed({
  get: () => props.searchQuery,
  set: (value) => emit("update:searchQuery", value),
});

const statusOptions = [
  { title: "全部结果", value: "all" },
  { title: "安全食品", value: "safe" },
  { title: "风险食品", value: "unsafe" },
];

const dateOptions = [
  { title: "全部时间", value: "all" },
  { title: "最近一周", value: "week" },
  { title: "最近一月", value: "month" },
  { title: "最近一年", value: "year" },
];

const applyFilters = () => {
  emit("applyFilters");
};
</script>

<style scoped>
.sticky-filters {
  position: sticky;
  top: 20px;
  z-index: 10;
}

.sticky-stats {
  position: sticky;
  top: calc(20px + 300px);
  z-index: 10;
}

@media (max-width: 960px) {
  .sticky-filters,
  .sticky-stats {
    position: static;
  }
}
</style>
