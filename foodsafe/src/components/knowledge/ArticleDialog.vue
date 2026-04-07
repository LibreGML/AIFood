<template>
  <v-dialog v-model="show" max-width="1000" scrollable>
    <v-card rounded="xl" v-if="currentArticle">
      <v-img :src="currentArticle.image" height="200" cover class="d-md-block"></v-img>
      <v-card-title class="text-h5 text-md-h4 font-weight-bold pa-4 pa-md-6">
        {{ currentArticle.title }}
      </v-card-title>
      <v-card-text class="pa-4 pa-md-6">
        <div
          class="d-flex flex-column flex-md-row align-start align-md-center mb-4 mb-md-6"
        >
          <div class="d-flex align-center">
            <v-avatar size="40" color="success">
              <span class="text-white font-weight-bold">专</span>
            </v-avatar>
            <div class="ml-3">
              <div class="font-weight-bold">食品安全专家</div>
              <div class="text-caption text-medium-emphasis">
                {{ currentArticle.date }}
              </div>
            </div>
          </div>
          <v-spacer class="d-none d-md-block"></v-spacer>
          <div class="d-flex flex-wrap ga-1 mt-2 mt-md-0">
            <v-chip
              v-for="(tag, i) in currentArticle.tags"
              :key="i"
              variant="tonal"
              rounded="pill"
              size="small"
              class="mr-1 mb-1"
            >
              {{ tag }}
            </v-chip>
          </div>
        </div>

        <div class="article-content">
          <p
            v-for="(paragraph, i) in currentArticle.content"
            :key="i"
            class="mb-3 mb-md-4"
          >
            {{ paragraph }}
          </p>
        </div>
      </v-card-text>
      <v-card-actions class="pa-4 pa-md-6">
        <v-btn
          color="success"
          rounded="pill"
          @click="close"
          block
          class="text-capitalize"
        >
          关闭
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  modelValue: Boolean,
  currentArticle: Object,
});

const emit = defineEmits(["update:modelValue"]);

const show = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const close = () => {
  emit("update:modelValue", false);
};
</script>

<style scoped>
.article-content p {
  font-size: 1rem;
  font-size: calc(1rem + 0.05vw);
  line-height: 1.6;
}
</style>
