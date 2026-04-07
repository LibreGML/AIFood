<template>
  <div class="scan-page">
    <AppBar />

    <v-container class="py-6 py-md-10">
      <v-row justify="center">
        <v-col cols="12" md="8">
          <h1 class="text-h4 text-md-h3 font-weight-bold text-center mb-2">
            AI植物病害检测
          </h1>
          <p class="text-subtitle-1 text-medium-emphasis text-center mb-8">
            拍摄植物叶片，快速识别植物病害类型及置信度
          </p>

          <ScanUploadSection
            :selectedImage="selectedImage"
            :isAnalyzing="isAnalyzing"
            @update:selectedImage="selectedImage = $event"
            @analyze="submitForAnalysis"
          />

          <ScanResultsSection
            v-if="analysisResult"
            :analysisResult="analysisResult"
            @newScan="startNewScan"
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import AppBar from "@/components/AppBar.vue";
import ScanResultsSection from "@/components/scan/ResultsSection.vue";
import ScanUploadSection from "@/components/scan/UploadSection.vue";
import { ref } from "vue";

const selectedImage = ref(null);
const isAnalyzing = ref(false);
const analysisResult = ref(null);

const submitForAnalysis = async () => {
  isAnalyzing.value = true;
  try {
    // 从 data URL 中提取 base64 数据
    const base64Image = selectedImage.value.split(",")[1];

    const response = await fetch("/infer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: base64Image }), // 直接发送 base64 字符串，而不是完整的 data URL
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();

    if (data.status === "success" && data.result) {
      // 处理返回的结果，提取置信度最高的病害
      const diseases = data.result;
      const topDisease = diseases[0]; // 结果已按置信度排序

      // 判断是否有病（置信度高于一定阈值）
      const hasDisease = topDisease.score > 0.1; // 降低阈值，提高敏感性

      analysisResult.value = {
        safe: !hasDisease,
        safetyScore: Math.round((1 - topDisease.score) * 100),
        foodInfo: {
          name: { label: "病害类型", value: topDisease.label },
          confidence: {
            label: "置信度",
            value: `${(topDisease.score * 100).toFixed(2)}%`,
          },
        },
        risks: hasDisease
          ? [
              {
                title: "植物病害",
                description: `检测到 ${topDisease.label}，置信度为 ${(
                  topDisease.score * 100
                ).toFixed(2)}%`,
              },
            ]
          : [],
        recommendation: hasDisease
          ? `建议立即采取措施处理 ${topDisease.label} 病害，可以使用相应的杀菌剂或生物防治方法。`
          : "未检测到明显的植物病害，继续保持良好的种植环境。",
      };
    } else {
      throw new Error(data.error || "检测失败");
    }
  } catch (error) {
    analysisResult.value = {
      safe: false,
      safetyScore: 0,
      foodInfo: {
        name: { label: "检测状态", value: "检测失败" },
      },
      risks: [
        {
          title: "网络错误",
          description:
            "无法连接到检测服务或检测过程中发生错误，请确保后端服务正在运行并可访问。",
        },
      ],
      recommendation: "请检查网络连接和后端服务状态，然后重试。",
    };
    console.error("检测过程中发生错误:", error);
  } finally {
    isAnalyzing.value = false;
  }
};

const startNewScan = () => {
  selectedImage.value = null;
  analysisResult.value = null;
};
</script>

<style scoped>
.scan-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
</style>
