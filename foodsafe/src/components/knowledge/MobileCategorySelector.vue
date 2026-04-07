<template>
  <v-select
    v-model="currentCategory"
    :items="categories"
    item-title="name"
    item-value="id"
    label="选择分类"
    variant="outlined"
    rounded="xl"
    hide-details
    class="mb-6"
  ></v-select>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  categories: Array,
  selectedCategory: String
})

const emit = defineEmits(['update:category'])

const currentCategory = computed({
  get: () => props.selectedCategory,
  set: (value) => emit('update:category', value)
})
</script>