<template>
  <v-card
    class="upload-card mb-8"
    rounded="xl"
    :class="{ 'drag-over': isDragOver }"
    @dragover.prevent="isDragOver = true"
    @dragleave.prevent="isDragOver = false"
    @drop.prevent="handleDrop"
  >
    <v-card-text class="pa-8 text-center">
      <div v-if="!selectedImage" class="upload-content">
        <v-icon size="64" color="success" class="mb-4">mdi-cloud-upload</v-icon>
        <h3 class="text-h5 font-weight-bold mb-2">拖拽图片到此处</h3>
        <p class="text-body-2 text-medium-emphasis mb-6">
          支持 JPG、PNG 格式，文件大小不超过 10MB
        </p>
        <v-btn color="success" size="large" rounded="pill" @click="triggerFileInput">
          <v-icon start>mdi-camera</v-icon>
          拍照或选择图片
        </v-btn>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          @change="handleFileSelect"
          style="display: none"
        />
      </div>

      <div v-else class="preview-content">
        <v-img
          :src="selectedImage"
          max-height="400"
          contain
          class="mb-4 rounded-lg"
        ></v-img>
        <div class="d-flex justify-center ga-4">
          <v-btn variant="outlined" rounded="pill" @click="clearImage"> 重新选择 </v-btn>
          <v-btn
            color="success"
            rounded="pill"
            @click="submitForAnalysis"
            :loading="isAnalyzing"
          >
            开始检测
          </v-btn>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  selectedImage: String,
  isAnalyzing: Boolean,
});

const emit = defineEmits(["update:selectedImage", "analyze"]);

const fileInput = ref(null);
const isDragOver = ref(false);

const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    processImageFile(file);
  }
};

const handleDrop = (event) => {
  isDragOver.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) {
    processImageFile(file);
  }
};

const processImageFile = (file) => {
  if (file.size > 10 * 1024 * 1024) {
    alert("文件大小不能超过10MB");
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    emit("update:selectedImage", e.target.result);
  };
  reader.readAsDataURL(file);
};

const clearImage = () => {
  emit("update:selectedImage", null);
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};

const submitForAnalysis = () => {
  emit("analyze");
};
</script>

<style scoped>
.upload-card {
  border: 2px dashed #cfd8dc;
  transition: all 0.3s ease;
}

.upload-card.drag-over {
  border-color: #4caf50;
  background-color: rgba(76, 175, 80, 0.05);
}
</style>
