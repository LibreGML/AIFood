<template>
  <v-card rounded="xl" class="mb-6">
    <v-card-text>
      <div
        class="d-flex flex-column flex-sm-row justify-space-between align-start align-sm-center ga-4"
      >
        <div>
          <h2 class="text-h5 font-weight-bold mb-1">
            {{ currentCategory.name }}
          </h2>
          <p class="text-body-2 text-medium-emphasis">
            {{ currentCategory.description }}
          </p>
        </div>
        <v-text-field
          v-model="searchQuery"
          placeholder="搜索知识库..."
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          rounded="pill"
          hide-details
          density="compact"
          class="search-field"
          style="max-width: 300px"
        ></v-text-field>
      </div>
    </v-card-text>
  </v-card>

  <v-row>
    <v-col cols="12" sm="6" lg="4" v-for="(article, i) in filteredArticles" :key="i">
      <v-card rounded="xl" class="h-100" @click="viewArticle(article)">
        <v-img :src="article.image" height="160" cover class="rounded-t-xl"></v-img>
        <v-card-title class="font-weight-bold">
          {{ article.title }}
        </v-card-title>
        <v-card-text>
          <p class="text-body-2 text-medium-emphasis mb-4">
            {{ article.excerpt }}
          </p>
          <div class="d-flex justify-space-between align-center">
            <div class="d-flex ga-2">
              <v-chip
                v-for="(tag, j) in article.tags.slice(0, 2)"
                :key="j"
                size="small"
                variant="tonal"
                rounded="pill"
              >
                {{ tag }}
              </v-chip>
            </div>
            <div class="text-caption text-medium-emphasis">
              {{ article.date }}
            </div>
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
import { ref } from "vue";

const props = defineProps({
  currentCategory: Object,
  filteredArticles: Array,
  totalPages: Number,
});

const emit = defineEmits(["viewArticle"]);

const searchQuery = ref("");
const currentPage = ref(1);

const viewArticle = (article) => {
  emit("viewArticle", article);
};
</script>

<style scoped>
.search-field :deep(.v-field) {
  border-radius: 50px !important;
}

:deep(.v-card) {
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
}
</style>
