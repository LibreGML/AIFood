<template>
  <v-card rounded="xl" class="mb-6">
    <v-card-title class="text-h6 font-weight-bold"> 知识分类 </v-card-title>
    <v-list nav>
      <v-list-item
        v-for="(category, i) in categories"
        :key="i"
        :title="category.name"
        :value="category.id"
        rounded="xl"
        class="mb-1 mx-2"
        :variant="selectedCategory === category.id ? 'tonal' : undefined"
        @click="selectCategory(category.id)"
      >
        <template v-slot:prepend>
          <v-icon :icon="category.icon"></v-icon>
        </template>
        <template v-slot:append>
          <v-chip
            size="small"
            variant="tonal"
            :color="selectedCategory === category.id ? 'success' : 'default'"
          >
            {{ category.count }}
          </v-chip>
        </template>
      </v-list-item>
    </v-list>
  </v-card>

  <v-card rounded="xl">
    <v-card-title class="text-h6 font-weight-bold"> 热门标签 </v-card-title>
    <v-card-text>
      <div class="d-flex flex-wrap ga-2">
        <v-chip
          v-for="(tag, i) in tags"
          :key="i"
          :color="selectedTag === tag ? 'success' : undefined"
          variant="outlined"
          rounded="pill"
          @click="toggleTag(tag)"
        >
          {{ tag }}
        </v-chip>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
const props = defineProps({
  categories: Array,
  tags: Array,
  selectedCategory: String,
  selectedTag: String,
});

const emit = defineEmits(["update:category", "update:tag"]);

const selectCategory = (categoryId) => {
  emit("update:category", categoryId);
};

const toggleTag = (tag) => {
  emit("update:tag", tag);
};
</script>
