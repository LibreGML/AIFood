<template>
  <div class="chat-header d-flex align-center py-3">
    <v-icon color="white" size="large" class="mr-2 ml-5">mdi-robot-outline</v-icon>
    <h2 class="text-h6 font-weight-bold text-white">AI 食品安全助手</h2>
    <v-spacer></v-spacer>
    <v-btn
      v-if="showClearButton"
      icon="mdi-delete-outline"
      variant="text"
      @click="clearChat"
      title="清空对话"
      color="white"
      size="small"
    ></v-btn>
  </div>
</template>

<script setup>
defineProps({
  showClearButton: Boolean,
});

const emit = defineEmits(["clearChat"]);

const clearChat = () => {
  emit("clearChat");
};
</script>

<style scoped lang="scss">
.chat-header {
  /*  */
  background: linear-gradient(120deg, #4caf50 0%, #2e7d32 100%);
  backdrop-filter: blur(10px);
  border-radius: 16px 16px 0 0;
  min-height: 48px;
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 8px 16px !important;
}
</style>
