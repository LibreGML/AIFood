<template>
  <div
    ref="chatContainer"
    class="chat-messages"
    :class="{ 'empty-chat': messages.length === 0 }"
  >
    <div
      v-if="messages.length === 0"
      class="empty-state d-flex flex-column align-center justify-center pa-4"
    >
      <div class="animation-container mb-4">
        <v-icon color="success" size="48" class="floating-icon"
          >mdi-robot-happy-outline</v-icon
        >
      </div>
      <h3 class="text-h6 font-weight-bold mb-2 text-success text-center">
        您好！我是您的食品安全AI助手
      </h3>
      <p class="text-medium-emphasis text-center mb-4 text-body-2">
        我可以帮您解答关于食品安全、营养搭配、食品检测等各类问题
      </p>
      <div class="quick-prompts mt-2">
        <v-chip
          v-for="(prompt, index) in quickPrompts"
          :key="index"
          class="ma-1 quick-chip"
          variant="outlined"
          color="success"
          @click="sendQuickPrompt(prompt)"
          size="small"
          rounded="lg"
        >
          {{ prompt }}
        </v-chip>
      </div>
    </div>

    <div v-else>
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.role]"
        class="d-flex pa-3"
      >
        <v-avatar
          :color="message.role === 'user' ? 'primary' : 'success'"
          size="28"
          class="flex-shrink-0 elevation-1"
        >
          <span
            class="text-white font-weight-bold text-caption"
            style="font-size: 0.7rem"
          >
            {{ message.role === "user" ? userInitial : "AI" }}
          </span>
        </v-avatar>

        <div class="message-content ml-2">
          <div
            class="font-weight-bold mb-1 d-flex align-center"
            :class="message.role === 'user' ? 'text-primary' : 'text-success'"
            style="font-size: 0.75rem"
          >
            <v-icon size="x-small" class="mr-1">{{
              message.role === "user" ? "mdi-account" : "mdi-robot-outline"
            }}</v-icon>
            <span class="text-caption">{{
              message.role === "user" ? "您" : "AI助手"
            }}</span>
          </div>

          <v-card
            :class="
              message.role === 'user' ? 'user-message-card' : 'assistant-message-card'
            "
            class="message-text elevation-0"
            rounded="lg"
          >
            <v-card-text class="pa-3">
              <div
                v-if="message.role === 'assistant' && typeof message.content === 'string'"
                v-html="renderMarkdown(message.content)"
              ></div>
              <div
                v-else-if="
                  message.role === 'assistant' && message.content.type === 'streaming'
                "
              >
                <div v-html="renderMarkdown(message.content.text)"></div>
                <v-progress-circular
                  v-if="message.content.text === ''"
                  indeterminate
                  size="16"
                  width="2"
                  color="success"
                  class="mt-1"
                ></v-progress-circular>
              </div>
              <div v-else>{{ message.content }}</div>
            </v-card-text>
          </v-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  messages: Array,
  userInitial: String,
  renderMarkdown: Function,
});

const emit = defineEmits(["sendQuickPrompt"]);

const chatContainer = ref(null);

const quickPrompts = [
  "如何判断食品是否变质？",
  "有机食品真的更安全吗？",
  "哪些食物不能一起吃？",
  "如何正确保存剩菜？",
  "食品添加剂安全吗？",
  "如何识别过期食品？",
];

const sendQuickPrompt = (prompt) => {
  emit("sendQuickPrompt", prompt);
};

defineExpose({
  chatContainer,
});
</script>

<style scoped lang="scss">
.chat-messages {
  flex: 1;
  overflow-y: auto;
  background-color: #fafafa;
  padding: 4px;

  &.empty-chat {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
  }
}

.message {
  margin-bottom: 4px;
  animation: fadeIn 0.3s ease-out;
  padding: 0 4px;

  &.user {
    .message-content {
      align-items: flex-end;
    }

    .user-message-card {
      background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
      border-top-right-radius: 0 !important;
      max-width: 85%;

      @media (min-width: 600px) {
        max-width: 75%;
      }
    }
  }

  &.assistant {
    .message-content {
      align-items: flex-start;
    }

    .assistant-message-card {
      background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%);
      border-top-left-radius: 0 !important;
      max-width: 85%;

      @media (min-width: 600px) {
        max-width: 75%;
      }
    }
  }
}

.message-content {
  display: flex;
  flex-direction: column;
  flex: 1;

  .message-text {
    white-space: pre-wrap;
    line-height: 1.3;
    font-size: 12px;
    padding: 0;

    :deep(.v-card-text) {
      padding: 4px 8px !important;
    }

    :deep(p) {
      margin-bottom: 0;

      &:last-child {
        margin-bottom: 0;
      }
    }

    :deep(ul),
    :deep(ol) {
      padding-left: 16px;
      margin: 0;
    }

    :deep(li) {
      margin-bottom: 0px;
    }

    :deep(pre) {
      background-color: #f5f5f5;
      padding: 4px;
      border-radius: 3px;
      overflow-x: auto;
      margin: 0;
      box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
      font-family: "Fira Code", monospace;
      font-size: 0.6rem;

      @media (min-width: 600px) {
        font-size: 0.65rem;
      }
    }

    :deep(code) {
      background-color: #f5f5f5;
      padding: 1px 2px;
      border-radius: 2px;
      font-family: "Fira Code", monospace;
      font-size: 0.75em;

      @media (min-width: 600px) {
        font-size: 0.8em;
      }
    }

    :deep(blockquote) {
      border-left: 2px solid #4caf50;
      padding-left: 8px;
      margin: 2px 0;
      color: #666;
    }

    :deep(h1),
    :deep(h2),
    :deep(h3) {
      margin: 4px 0 0px 0;
      color: #2e7d32;
    }

    :deep(h1) {
      font-size: 1rem;
    }

    :deep(h2) {
      font-size: 0.95rem;
    }

    :deep(h3) {
      font-size: 0.9rem;
    }
  }
}

.empty-state {
  text-align: center;
  max-width: 100%;
  margin: 0 auto;
  padding: 8px;

  .animation-container {
    position: relative;
    width: 60px;
    height: 60px;

    .floating-icon {
      animation: float 3s ease-in-out infinite;
    }
  }

  .quick-prompts {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 4px;
    margin-top: 8px;
    width: 100%;
  }

  .quick-chip {
    transition: all 0.3s ease;
    max-width: 90%;
    font-size: 0.75rem;
    padding: 4px 8px;

    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
  }

  h3 {
    font-size: 1rem !important;
    margin-bottom: 8px !important;
  }

  p {
    font-size: 0.8rem !important;
    margin-bottom: 8px !important;
  }

  @media (min-width: 600px) {
    h3 {
      font-size: 1.1rem !important;
    }

    p {
      font-size: 0.9rem !important;
    }
  }
}

// 滚动条样式
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #4caf50, #2e7d32);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #43a047, #1b5e20);
}

// 动画
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
}

// 移动端优化
@media (max-width: 599px) {
  .message-content {
    .message-text {
      font-size: 0.8125rem;

      :deep(pre) {
        font-size: 0.7rem;
        padding: 10px;
      }

      :deep(code) {
        font-size: 0.7em;
      }
    }
  }

  .empty-state {
    h3 {
      font-size: 1rem !important;
    }

    p {
      font-size: 0.8rem !important;
    }
  }

  .message {
    padding: 10px !important;
    margin-bottom: 10px;
  }
}
</style>
