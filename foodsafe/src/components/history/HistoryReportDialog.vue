import { computed } from "vue";

<template>
  <v-dialog v-model="show" max-width="1000" scrollable>
    <v-card rounded="xl" v-if="currentRecord">
      <v-card-title class="pa-6 bg-success-lighten-5">
        <div class="d-flex align-center">
          <v-img
            :src="currentRecord.image"
            width="60"
            height="60"
            cover
            class="rounded mr-4"
          ></v-img>
          <div>
            <div class="text-h5 font-weight-bold">{{ currentRecord.foodName }}</div>
            <div class="text-medium-emphasis">{{ currentRecord.brand }}</div>
          </div>
          <v-spacer></v-spacer>
          <v-chip
            :color="currentRecord.status === 'safe' ? 'success' : 'error'"
            size="large"
            label
          >
            {{ currentRecord.status === "safe" ? "安全" : "存在风险" }}
          </v-chip>
        </div>
      </v-card-title>

      <v-card-text class="pa-6">
        <v-row>
          <v-col cols="12" md="4">
            <v-card
              :color="
                currentRecord.status === 'safe' ? 'success-lighten-5' : 'error-lighten-5'
              "
              rounded="lg"
              class="mb-4"
            >
              <v-card-text class="text-center py-6">
                <div class="text-h3 font-weight-bold mb-2">
                  {{ currentRecord.safetyScore }}<span class="text-h5">分</span>
                </div>
                <div class="text-subtitle-1">安全指数</div>
              </v-card-text>
            </v-card>

            <v-card rounded="lg" class="mb-4">
              <v-card-title class="text-subtitle-1 font-weight-bold d-flex align-center">
                <v-icon start>mdi-information</v-icon>
                检测信息
              </v-card-title>
              <v-card-text>
                <div class="d-flex justify-space-between mb-2">
                  <div class="text-medium-emphasis">检测时间:</div>
                  <div>{{ currentRecord.date }}</div>
                </div>
                <div class="d-flex justify-space-between mb-2">
                  <div class="text-medium-emphasis">检测方式:</div>
                  <div>AI图像识别</div>
                </div>
                <div class="d-flex justify-space-between">
                  <div class="text-medium-emphasis">检测编号:</div>
                  <div>{{ currentRecord.id }}</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="8">
            <v-card rounded="lg" class="mb-4">
              <v-card-title class="text-subtitle-1 font-weight-bold d-flex align-center">
                <v-icon start>mdi-food</v-icon>
                食品信息
              </v-card-title>
              <v-card-text>
                <v-list lines="two">
                  <v-list-item v-for="(info, key) in currentRecord.foodInfo" :key="key">
                    <v-list-item-title>{{ info.label }}</v-list-item-title>
                    <v-list-item-subtitle>{{ info.value }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <v-card
              v-if="currentRecord.status !== 'safe'"
              color="error-lighten-5"
              rounded="lg"
              class="mb-4"
            >
              <v-card-title class="text-subtitle-1 font-weight-bold d-flex align-center">
                <v-icon color="error" class="mr-2">mdi-alert-circle</v-icon>
                风险提示
              </v-card-title>
              <v-card-text>
                <div v-for="(risk, i) in currentRecord.risks" :key="i" class="mb-2">
                  <strong>{{ risk.title }}:</strong> {{ risk.description }}
                </div>
              </v-card-text>
            </v-card>

            <v-card rounded="lg">
              <v-card-title class="text-subtitle-1 font-weight-bold d-flex align-center">
                <v-icon start>mdi-doctor</v-icon>
                专家建议
              </v-card-title>
              <v-card-text>
                {{ currentRecord.recommendation }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions class="pa-6">
        <v-btn variant="outlined" rounded="pill" @click="downloadReport">
          <v-icon start>mdi-download</v-icon>
          下载报告
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="success" rounded="pill" @click="close"> 关闭 </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  modelValue: Boolean,
  currentRecord: Object,
});

const emit = defineEmits(["update:modelValue"]);

const show = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const close = () => {
  emit("update:modelValue", false);
};

const downloadReport = () => {
  alert("报告下载功能已触发");
};
</script>
