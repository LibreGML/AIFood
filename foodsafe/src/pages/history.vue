<template>
  <div class="history-page">
    <AppBar />

    <v-container class="py-6 py-md-10">
      <v-row>
        <v-col cols="12">
          <HistoryHeader />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="3">
          <HistoryFilterSection
            :stats="stats"
            :filterStatus="filterStatus"
            :filterDate="filterDate"
            :searchQuery="searchQuery"
            @update:filterStatus="filterStatus = $event"
            @update:filterDate="filterDate = $event"
            @update:searchQuery="searchQuery = $event"
            @applyFilters="applyFilters"
          />
        </v-col>

        <v-col cols="12" md="9">
          <HistoryRecordListView
            :filteredHistory="filteredHistory"
            :viewMode="viewMode"
            @update:viewMode="viewMode = $event"
            @viewReport="viewReport"
          />
        </v-col>
      </v-row>
    </v-container>

    <v-btn
      color="success"
      icon="mdi-plus"
      size="large"
      fixed
      bottom
      right
      rounded="circle"
      class="d-sm-none mb-4 ml-4"
      @click="$router.push('/scan')"
    ></v-btn>

    <HistoryReportDialog v-model="showReport" :currentRecord="currentRecord" />
  </div>
</template>

<script setup>
import AppBar from "@/components/AppBar.vue";
import HistoryFilterSection from "@/components/history/HistoryFilterSection.vue";
import HistoryHeader from "@/components/history/HistoryHeader.vue";
import HistoryRecordListView from "@/components/history/HistoryRecordListView.vue";
import HistoryReportDialog from "@/components/history/HistoryReportDialog.vue";
import { computed, ref } from "vue";

const filterStatus = ref("all");
const filterDate = ref("all");
const searchQuery = ref("");
const viewMode = ref("grid");
const showReport = ref(false);
const currentRecord = ref(null);
const currentPage = ref(1);
const itemsPerPage = ref(10);

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

const headers = [
  { title: "食品信息", key: "foodName" },
  { title: "检测结果", key: "status", align: "center" },
  { title: "安全指数", key: "safetyScore", align: "center" },
  { title: "检测时间", key: "date", align: "center" },
  { title: "操作", key: "actions", align: "center", sortable: false },
];

const historyData = [
  {
    id: "20251024001",
    foodName: "蒙牛纯牛奶",
    brand: "蒙牛",
    status: "safe",
    safetyScore: 92,
    date: "2025-10-24 14:30",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
    foodInfo: {
      name: { label: "食品名称", value: "蒙牛纯牛奶" },
      brand: { label: "品牌", value: "蒙牛" },
      productionDate: { label: "生产日期", value: "2025-10-01" },
      expirationDate: { label: "保质期", value: "2026-04-01" },
      ingredients: { label: "配料表", value: "生牛乳" },
    },
    recommendation:
      "产品安全可靠，建议在保质期内饮用完毕，开启后请冷藏并在24小时内饮用完毕",
  },
  {
    id: "20251023015",
    foodName: "康师傅红烧牛肉面",
    brand: "康师傅",
    status: "unsafe",
    safetyScore: 65,
    date: "2025-10-23 12:15",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
    foodInfo: {
      name: { label: "食品名称", value: "康师傅红烧牛肉面" },
      brand: { label: "品牌", value: "康师傅" },
      productionDate: { label: "生产日期", value: "2025-07-15" },
      expirationDate: { label: "保质期", value: "2026-01-15" },
      ingredients: { label: "配料表", value: "小麦粉、牛肉、食用盐、香辛料" },
    },
    risks: [
      {
        title: "钠含量过高",
        description: "每100g含钠1200mg，超出推荐值50%，长期食用可能增加高血压风险",
      },
    ],
    recommendation:
      "建议适量食用，高血压患者应谨慎选择。搭配富含钾的食物如香蕉、橙子等有助于钠的排出",
  },
  {
    id: "20251022008",
    foodName: "伊利金典有机奶",
    brand: "伊利",
    status: "safe",
    safetyScore: 96,
    date: "2025-10-22 09:45",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
    foodInfo: {
      name: { label: "食品名称", value: "伊利金典有机奶" },
      brand: { label: "品牌", value: "伊利" },
      productionDate: { label: "生产日期", value: "2025-09-20" },
      expirationDate: { label: "保质期", value: "2026-03-20" },
      ingredients: { label: "配料表", value: "有机生牛乳" },
    },
    recommendation: "有机产品，品质优良，可放心饮用",
  },
  {
    id: "20251020022",
    foodName: "统一老坛酸菜牛肉面",
    brand: "统一",
    status: "unsafe",
    safetyScore: 58,
    date: "2025-10-20 18:20",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
    foodInfo: {
      name: { label: "食品名称", value: "统一老坛酸菜牛肉面" },
      brand: { label: "品牌", value: "统一" },
      productionDate: { label: "生产日期", value: "2025-06-05" },
      expirationDate: { label: "保质期", value: "2025-12-05" },
      ingredients: { label: "配料表", value: "小麦粉、酸菜、牛肉、食用盐、香辛料" },
    },
    risks: [
      {
        title: "钠含量过高",
        description: "每100g含钠1350mg，超出推荐值65%，长期食用可能增加高血压风险",
      },
      {
        title: "脂肪含量偏高",
        description: "每100g含脂肪18g，占营养素参考值30%，过量摄入可能导致肥胖",
      },
    ],
    recommendation: "建议偶尔食用，不宜长期大量摄入。高血压、高血脂患者应避免食用",
  },
  {
    id: "20251018011",
    foodName: "农夫山泉矿泉水",
    brand: "农夫山泉",
    status: "safe",
    safetyScore: 98,
    date: "2025-10-18 11:30",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
    foodInfo: {
      name: { label: "食品名称", value: "农夫山泉矿泉水" },
      brand: { label: "品牌", value: "农夫山泉" },
      productionDate: { label: "生产日期", value: "2025-09-10" },
      expirationDate: { label: "保质期", value: "2026-09-10" },
      ingredients: { label: "配料表", value: "天然矿泉水" },
    },
    recommendation: "天然矿泉水，品质可靠，可放心饮用",
  },
  {
    id: "20251015003",
    foodName: "德芙巧克力",
    brand: "德芙",
    status: "unsafe",
    safetyScore: 72,
    date: "2025-10-15 16:45",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
    foodInfo: {
      name: { label: "食品名称", value: "德芙巧克力" },
      brand: { label: "品牌", value: "德芙" },
      productionDate: { label: "生产日期", value: "2025-08-20" },
      expirationDate: { label: "保质期", value: "2026-02-20" },
      ingredients: { label: "配料表", value: "可可液块、白砂糖、可可脂、乳粉、乳化剂" },
    },
    risks: [
      {
        title: "糖分含量高",
        description: "每100g含糖58g，占营养素参考值约20%，过量摄入可能导致血糖升高",
      },
    ],
    recommendation: "建议适量食用，糖尿病患者应谨慎选择。最好在两餐之间作为加餐食用",
  },
  {
    id: "20251012017",
    foodName: "金龙鱼花生油",
    brand: "金龙鱼",
    status: "safe",
    safetyScore: 88,
    date: "2025-10-12 10:20",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
    foodInfo: {
      name: { label: "食品名称", value: "金龙鱼花生油" },
      brand: { label: "品牌", value: "金龙鱼" },
      productionDate: { label: "生产日期", value: "2025-07-10" },
      expirationDate: { label: "保质期", value: "2027-07-10" },
      ingredients: { label: "配料表", value: "花生油" },
    },
    recommendation: "食用植物调和油，建议按需取用，避免高温烹饪",
  },
  {
    id: "20251010009",
    foodName: "洽洽瓜子",
    brand: "洽洽",
    status: "unsafe",
    safetyScore: 67,
    date: "2025-10-10 15:30",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
    foodInfo: {
      name: { label: "食品名称", value: "洽洽瓜子" },
      brand: { label: "品牌", value: "洽洽" },
      productionDate: { label: "生产日期", value: "2025-06-15" },
      expirationDate: { label: "保质期", value: "2025-12-15" },
      ingredients: { label: "配料表", value: "葵花籽、食用盐、香辛料" },
    },
    risks: [
      {
        title: "钠含量偏高",
        description: "每100g含钠850mg，超出推荐值35%，长期食用可能影响血压",
      },
      {
        title: "脂肪含量较高",
        description: "每100g含脂肪49g，占营养素参考值80%，过量摄入易导致肥胖",
      },
    ],
    recommendation: "建议控制食用量，每次不超过25g。高血压和肥胖人群应减少摄入",
  },
];

const stats = computed(() => {
  const safe = historyData.filter((item) => item.status === "safe").length;
  const unsafe = historyData.filter((item) => item.status === "unsafe").length;
  return {
    safe,
    unsafe,
    total: historyData.length,
  };
});

const filteredHistory = computed(() => {
  let result = historyData;

  if (filterStatus.value !== "all") {
    const status = filterStatus.value === "safe" ? "safe" : "unsafe";
    result = result.filter((item) => item.status === status);
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(
      (item) =>
        item.foodName.toLowerCase().includes(query) ||
        item.brand.toLowerCase().includes(query)
    );
  }

  if (filterDate.value !== "all") {
    const now = new Date();
    result = result.filter((item) => {
      const itemDate = new Date(item.date);
      switch (filterDate.value) {
        case "week":
          const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
          return itemDate >= weekAgo;
        case "month":
          const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
          return itemDate >= monthAgo;
        case "year":
          const yearAgo = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
          return itemDate >= yearAgo;
        default:
          return true;
      }
    });
  }

  return result;
});

const paginatedHistory = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredHistory.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(filteredHistory.value.length / itemsPerPage.value);
});

const applyFilters = () => {
  currentPage.value = 1;
};

const viewReport = (record) => {
  currentRecord.value = record;
  showReport.value = true;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("zh-CN");
};
</script>

<style scoped>
.history-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
</style>
