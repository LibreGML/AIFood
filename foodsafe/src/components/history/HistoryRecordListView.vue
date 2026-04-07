<template>
  <v-card rounded="xl" class="mb-6">
    <v-card-text>
      <div
        class="d-flex flex-column flex-sm-row justify-space-between align-start align-sm-center ga-4"
      >
        <div>
          <h2 class="text-h5 font-weight-bold mb-1">检测记录</h2>
          <p class="text-body-2 text-medium-emphasis">
            共 {{ filteredHistory.length }} 条记录
          </p>
        </div>
        <div class="d-flex ga-2">
          <v-btn
            :variant="viewMode === 'list' ? 'tonal' : 'outlined'"
            icon="mdi-format-list-bulleted"
            rounded="circle"
            @click="setViewMode('list')"
          ></v-btn>
          <v-btn
            :variant="viewMode === 'grid' ? 'tonal' : 'outlined'"
            icon="mdi-grid"
            rounded="circle"
            @click="setViewMode('grid')"
          ></v-btn>
        </div>
      </div>
    </v-card-text>
  </v-card>

  <v-card v-if="viewMode === 'list'" rounded="xl" class="overflow-hidden">
    <v-data-table
      :headers="headers"
      :items="filteredHistory"
      :items-per-page="10"
      class="rounded-xl"
      hide-default-footer
    >
      <template v-slot:item.foodName="{ item }">
        <div class="d-flex align-center">
          <v-img
            :src="item.image"
            width="50"
            height="50"
            cover
            class="rounded mr-3"
          ></v-img>
          <div>
            <div class="font-weight-bold">{{ item.foodName }}</div>
            <div class="text-caption text-medium-emphasis">{{ item.brand }}</div>
          </div>
        </div>
      </template>

      <template v-slot:item.status="{ item }">
        <v-chip :color="item.status === 'safe' ? 'success' : 'error'" size="small" label>
          {{ item.status === "safe" ? "安全" : "存在风险" }}
        </v-chip>
      </template>

      <template v-slot:item.safetyScore="{ item }">
        <div class="d-flex align-center">
          <v-progress-circular
            :model-value="item.safetyScore"
            :color="
              item.safetyScore > 80
                ? 'success'
                : item.safetyScore > 60
                ? 'warning'
                : 'error'
            "
            size="30"
            width="3"
            class="mr-2"
          >
            <span class="text-caption">{{ item.safetyScore }}</span>
          </v-progress-circular>
          <span>{{ item.safetyScore }}分</span>
        </div>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-btn variant="outlined" size="small" rounded="pill" @click="viewReport(item)">
          查看详情
        </v-btn>
      </template>
    </v-data-table>
  </v-card>

  <v-row v-else>
    <v-col cols="12" sm="6" lg="4" v-for="(record, i) in paginatedHistory" :key="i">
      <v-card rounded="xl" class="h-100">
        <v-img :src="record.image" aspect-ratio="16/9" cover class="rounded-t-xl"></v-img>
        <v-card-title class="font-weight-bold">
          {{ record.foodName }}
        </v-card-title>
        <v-card-text>
          <div class="d-flex align-center mb-2">
            <div class="text-body-2 text-medium-emphasis">品牌:</div>
            <div class="ml-auto font-weight-bold">{{ record.brand }}</div>
          </div>

          <div class="d-flex align-center mb-2">
            <div class="text-body-2 text-medium-emphasis">检测时间:</div>
            <div class="ml-auto font-weight-bold">{{ formatDate(record.date) }}</div>
          </div>

          <div class="d-flex align-center mb-4">
            <div class="text-body-2 text-medium-emphasis">安全指数:</div>
            <div class="ml-auto">
              <v-progress-linear
                :model-value="record.safetyScore"
                :color="
                  record.safetyScore > 80
                    ? 'success'
                    : record.safetyScore > 60
                    ? 'warning'
                    : 'error'
                "
                height="8"
                rounded
              ></v-progress-linear>
            </div>
          </div>

          <div class="d-flex justify-space-between align-center">
            <v-chip
              :color="record.status === 'safe' ? 'success' : 'error'"
              size="small"
              label
            >
              {{ record.status === "safe" ? "安全" : "存在风险" }}
            </v-chip>
            <v-btn
              variant="outlined"
              size="small"
              rounded="pill"
              @click="viewReport(record)"
            >
              查看详情
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <div class="d-flex justify-center mt-6">
    <v-pagination
      v-model="currentPage"
      :length="totalPages"
      rounded="circle"
    ></v-pagination>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";

const props = defineProps({
  filteredHistory: Array,
  viewMode: String,
});

const emit = defineEmits(["update:viewMode", "viewReport"]);

const currentPage = ref(1);
const itemsPerPage = ref(10);

const headers = [
  { title: "食品信息", key: "foodName" },
  { title: "检测结果", key: "status", align: "center" },
  { title: "安全指数", key: "safetyScore", align: "center" },
  { title: "检测时间", key: "date", align: "center" },
  { title: "操作", key: "actions", align: "center", sortable: false },
];

const paginatedHistory = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return props.filteredHistory.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(props.filteredHistory.length / itemsPerPage.value);
});

const setViewMode = (mode) => {
  emit("update:viewMode", mode);
};

const viewReport = (record) => {
  emit("viewReport", record);
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("zh-CN");
};
</script>

<style scoped>
:deep(.v-data-table .v-data-table__td) {
  padding: 12px 16px !important;
}

:deep(.v-data-table .v-data-table__th) {
  padding: 8px 16px !important;
}

:deep(.v-card) {
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }
}
</style>
