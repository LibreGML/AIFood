<template>
  <div class="knowledge-page">
    <AppBar />

    <v-container class="py-6 py-md-10">
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 text-md-h3 font-weight-bold text-center mb-2">
            食品安全知识库
          </h1>
          <p class="text-subtitle-1 text-medium-emphasis text-center mb-8">
            获取专业的食品安全知识和实用建议
          </p>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="3" class="d-none d-md-block">
          <KnowledgeCategorySidebar
            :categories="categories"
            :tags="tags"
            :selectedCategory="selectedCategory"
            :selectedTag="selectedTag"
            @update:category="selectedCategory = $event"
            @update:tag="toggleTag"
          />
        </v-col>

        <v-col cols="12" class="d-md-none">
          <KnowledgeMobileCategorySelector
            :categories="categories"
            :selectedCategory="selectedCategory"
            @update:category="selectedCategory = $event"
          />
        </v-col>

        <v-col cols="12" :md="9">
          <KnowledgeArticleList
            :currentCategory="currentCategory"
            :filteredArticles="filteredArticles"
            :totalPages="totalPages"
            @viewArticle="viewArticle"
          />
        </v-col>
      </v-row>
    </v-container>

    <KnowledgeArticleDialog v-model="showArticle" :currentArticle="currentArticle" />
  </div>
</template>

<script setup>
import AppBar from "@/components/AppBar.vue";
import KnowledgeArticleDialog from "@/components/knowledge/ArticleDialog.vue";
import KnowledgeArticleList from "@/components/knowledge/ArticleList.vue";
import KnowledgeCategorySidebar from "@/components/knowledge/CategorySidebar.vue";
import KnowledgeMobileCategorySelector from "@/components/knowledge/MobileCategorySelector.vue";
import { computed, ref } from "vue";

const selectedCategory = ref("all");
const selectedTag = ref("");
const showArticle = ref(false);
const currentArticle = ref(null);

const categories = [
  {
    id: "all",
    name: "全部",
    icon: "mdi-view-grid",
    count: 28,
    description: "所有食品安全相关知识",
  },
  {
    id: "preservatives",
    name: "食品添加剂",
    icon: "mdi-test-tube",
    count: 5,
    description: "食品添加剂的作用和安全性",
  },
  {
    id: "storage",
    name: "储存方法",
    icon: "mdi-fridge",
    count: 4,
    description: "不同食品的正确储存方式",
  },
  {
    id: "nutrition",
    name: "营养成分",
    icon: "mdi-nutrition",
    count: 7,
    description: "食品营养成分解析",
  },
  {
    id: "contamination",
    name: "食品污染",
    icon: "mdi-bacteria",
    count: 6,
    description: "食品污染类型及预防措施",
  },
  {
    id: "standards",
    name: "安全标准",
    icon: "mdi-file-certificate",
    count: 6,
    description: "国家食品安全标准解读",
  },
];

const tags = [
  "添加剂",
  "防腐剂",
  "营养",
  "储存",
  "保质期",
  "污染",
  "细菌",
  "农药残留",
  "重金属",
  "过敏原",
];

const articles = [
  {
    id: 1,
    title: "食品添加剂真的有害吗？",
    excerpt: "深入了解食品添加剂的作用机制和安全标准，消除对食品添加剂的误解",
    content: [
      "食品添加剂是现代食品工业的重要组成部分，在食品生产中发挥着重要作用。很多人对食品添加剂存在误解，认为它们都是有害的。实际上，合法使用的食品添加剂是经过严格安全性评估的，其使用量也在安全范围内。",
      "食品添加剂主要有以下几个作用：1. 保持食品的营养价值；2. 防止食品腐败变质，延长保质期；3. 改善食品的感官性状，如色泽、香味、口感等；4. 便于食品的生产、加工、包装、运输或者贮藏。",
      "我国对食品添加剂的使用有严格的标准和规定。《食品安全国家标准 食品添加剂使用标准》(GB 2760)明确规定了食品添加剂的使用范围和使用量。只要按照标准使用，食品添加剂是安全的。",
      "消费者在选择食品时，应注意查看食品标签，了解食品添加剂的种类和含量。对于某些敏感人群，如过敏体质者，应特别注意避免摄入可能引起过敏的食品添加剂。",
    ],
    category: "preservatives",
    tags: ["添加剂", "防腐剂", "安全标准"],
    date: "2025-10-15",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
  },
  {
    id: 2,
    title: "如何正确储存各类食品？",
    excerpt: "不同食品的储存方法和注意事项，延长食品保质期，确保食品安全",
    content: [
      "正确的食品储存方法不仅能延长食品的保质期，还能确保食品的营养价值和安全性。不同类型的食品需要不同的储存条件。",
      "蔬菜水果类：大多数蔬菜水果应存放在阴凉、通风、避光的地方。部分水果如香蕉、芒果等热带水果不宜放冰箱。绿叶蔬菜可用保鲜袋包装后放入冰箱冷藏室。",
      "肉类和海鲜：生肉和海鲜应尽快食用，如需储存应放入冰箱冷冻室。包装好的肉类在冷冻条件下可保存3-6个月。解冻时应提前放入冷藏室缓慢解冻，避免在室温下解冻。",
      "干货和调料：米面粮油等干货应存放在干燥、通风、避光的地方，避免受潮和虫害。开封后应密封保存。调料应远离热源和湿气，避免变质。",
      "乳制品：乳制品应严格按照包装上的储存条件存放，通常需要冷藏。开封后应尽快食用完毕，并注意观察是否有异味或变质现象。",
    ],
    category: "storage",
    tags: ["储存", "保质期"],
    date: "2025-10-10",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
  },
  {
    id: 3,
    title: "解读食品标签的营养成分表",
    excerpt: "学会看懂食品标签，了解食品的营养信息，做出更健康的食品选择",
    content: [
      "食品标签上的营养成分表是消费者了解食品营养价值的重要途径。正确理解营养成分表有助于我们做出更健康的食品选择。",
      "营养成分表通常包含能量和几种核心营养素的含量：蛋白质、脂肪、碳水化合物和钠。这些成分的含量通常以每100克(毫升)食品或每份食品为单位标示。",
      "能量：单位为千焦(kJ)或千卡(kcal)，表示食品提供给人体的热量。注意区分每100克和每份的热量，避免摄入过多热量。",
      "蛋白质：是构成人体组织的基本物质，对维持身体健康至关重要。一般而言，蛋白质含量越高，食品的营养价值越高。",
      "脂肪：包括饱和脂肪和不饱和脂肪。过多摄入饱和脂肪可能增加心血管疾病风险，而不饱和脂肪对人体有益。",
      "碳水化合物：人体主要的能量来源。注意区分糖分和膳食纤维的含量，高糖食品应适量摄入。",
      "钠：即食盐的成分，摄入过多可能导致高血压。世界卫生组织建议成人每日钠摄入量不超过2000毫克。",
    ],
    category: "nutrition",
    tags: ["营养", "标签"],
    date: "2025-10-05",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
  },
  {
    id: 4,
    title: "常见的食品污染类型及预防",
    excerpt: "了解食品污染的主要类型和预防措施，保护您和家人的饮食安全",
    content: [
      "食品污染是指食品在生产、加工、运输、储存、销售和食用过程中，受到有害物质的侵袭，导致食品的营养价值和食用价值降低，甚至对人体健康造成危害。",
      "生物性污染：这是最常见的食品污染类型，主要包括细菌、病毒、寄生虫和霉菌等微生物污染。沙门氏菌、大肠杆菌、金黄色葡萄球菌等都是常见的致病菌。预防措施包括保持清洁、生熟分开、充分加热、安全温度储存等。",
      "化学性污染：包括农药残留、重金属、工业化学品等。农药残留主要来源于农作物种植过程中使用的杀虫剂、除草剂等。重金属污染主要来源于环境污染，如铅、汞、镉等。预防措施包括选择正规渠道购买食品、充分清洗、多样化饮食等。",
      "物理性污染：指食品中混入的异物，如灰尘、金属碎片、毛发等。这类污染虽然不一定会导致疾病，但会影响食品的感官性状和食用安全性。预防措施包括加强食品生产过程的卫生管理、使用合格的包装材料等。",
      "为预防食品污染，消费者应选择正规渠道购买食品，注意查看食品标签和生产日期，正确储存食品，加工食品时保持清洁，充分加热，避免交叉污染。",
    ],
    category: "contamination",
    tags: ["污染", "细菌", "农药残留", "重金属"],
    date: "2025-09-28",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
  },
];

const currentCategory = computed(() => {
  return categories.find((c) => c.id === selectedCategory.value) || categories[0];
});

const filteredArticles = computed(() => {
  let result = articles;

  if (selectedCategory.value !== "all") {
    result = result.filter((article) => article.category === selectedCategory.value);
  }

  if (selectedTag.value) {
    result = result.filter((article) => article.tags.includes(selectedTag.value));
  }

  return result;
});

const totalPages = computed(() => {
  let count = articles.length;

  if (selectedCategory.value !== "all") {
    count = articles.filter((article) => article.category === selectedCategory.value)
      .length;
  }

  return Math.ceil(count / 6);
});

const toggleTag = (tag) => {
  selectedTag.value = selectedTag.value === tag ? "" : tag;
};

const viewArticle = (article) => {
  currentArticle.value = article;
  showArticle.value = true;
};
</script>

<style scoped>
.knowledge-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
</style>
