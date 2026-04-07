<template>
  <div class="chat-input">
    <div class="input-container elevation-4">
      <v-form @submit.prevent="sendMessage" class="d-flex align-center">
        <v-textarea
          v-model="inputMessage"
          rows="1"
          max-rows="5"
          placeholder="输入消息... (Ctrl+Enter发送)"
          variant="solo-filled"
          hide-details
          class="flex-grow-1 message-input"
          :disabled="disabled"
          @keydown="handleKeyDown"
          auto-grow
          flat
        ></v-textarea>

        <div class="button-group d-flex align-center">
          <v-btn
            v-if="inputMessage.trim()"
            icon="mdi-emoticon-happy-outline"
            variant="text"
            size="large"
            class="emoji-button"
            @click="toggleEmojiPicker"
          ></v-btn>

          <v-btn
            v-if="!inputMessage.trim() && !isRecording"
            icon="mdi-microphone"
            variant="text"
            size="small"
            class="record-button"
            @click="toggleRecording"
            :color="isRecording ? 'error' : 'grey-darken-1'"
          ></v-btn>

          <v-btn
            v-if="inputMessage.trim() || isRecording"
            type="submit"
            :icon="inputMessage.trim() ? 'mdi-send' : 'mdi-close'"
            size="small"
            variant="elevated"
            :color="inputMessage.trim() ? 'primary' : 'grey-lighten-1'"
            class="send-button ml-2"
            elevation="2"
          ></v-btn>
        </div>
      </v-form>
    </div>

    <div class="input-footer d-flex align-center justify-space-between mt-2">
      <div class="text-caption text-medium-emphasis d-flex align-center">
        <v-icon size="x-small" class="mr-1">mdi-information-outline</v-icon>
        <span>AI助手可能出错，请核实重要信息</span>
      </div>

      <div class="recording-indicator" v-if="isRecording">
        <v-icon size="x-small" color="red" class="mr-1">mdi-record-circle</v-icon>
        <span class="text-caption text-red">录音中...</span>
      </div>
    </div>

    <div v-if="showEmojiPicker" class="emoji-picker elevation-8">
      <div class="emoji-header d-flex justify-space-between align-center pa-2">
        <span class="text-body-2 font-weight-medium">选择表情</span>
        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          @click="toggleEmojiPicker"
        ></v-btn>
      </div>
      <div class="emoji-grid pa-2">
        <span
          v-for="emoji in emojis"
          :key="emoji"
          @click="addEmoji(emoji)"
          class="emoji-item d-flex align-center justify-center"
        >
          {{ emoji }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  disabled: Boolean,
});

const emit = defineEmits(["sendMessage", "update:inputMessage"]);

const inputMessage = ref("");
const showEmojiPicker = ref(false);
const isRecording = ref(false);

const emojis = [
  "😀",
  "😂",
  "😍",
  "🥰",
  "😎",
  "🤩",
  "🥳",
  "😭",
  "😡",
  "🤯",
  "👍",
  "👎",
  "👌",
  "✌️",
  "🤞",
  "🤟",
  "🤘",
  "👏",
  "🙌",
  "👐",
  "🐶",
  "🐱",
  "🐭",
  "🐹",
  "🐰",
  "🦊",
  "🐻",
  "🐼",
  "🐨",
  "🐯",
  "🍎",
  "🍊",
  "🍋",
  "🍌",
  "🍉",
  "🍇",
  "🍓",
  "🍒",
  "🍑",
  "🥭",
  "🍕",
  "🍔",
  "🍟",
  "🌭",
  "🍿",
  "🍦",
  "🍩",
  "🍪",
  "🎂",
  "🍫",
];

const sendMessage = () => {
  if (inputMessage.value.trim() && !isRecording.value) {
    emit("sendMessage", inputMessage.value);
    inputMessage.value = "";
    showEmojiPicker.value = false;
  } else if (isRecording.value) {
    // 停止录音
    toggleRecording();
  }
};

const handleKeyDown = (event) => {
  if (event.key === "Enter" && event.ctrlKey) {
    event.preventDefault();
    sendMessage();
  }
};

const toggleEmojiPicker = () => {
  showEmojiPicker.value = !showEmojiPicker.value;
};

const addEmoji = (emoji) => {
  inputMessage.value += emoji;
  showEmojiPicker.value = false;
};

const toggleRecording = () => {
  isRecording.value = !isRecording.value;
};

defineExpose({
  inputMessage,
});
</script>

<style scoped lang="scss">
.chat-input {
  background: linear-gradient(135deg, #f0f4f8 0%, #e6ecf2 100%);
  padding: 8px 12px !important;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  position: sticky;
  bottom: 0;
  backdrop-filter: blur(10px);

  .input-container {
    background: white;
    border-radius: 24px;
    padding: 4px 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08) !important;

    &:hover {
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12) !important;
    }

    &:focus-within {
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
    }

    :deep(.v-textarea) {
      .v-field {
        border-radius: 20px;
        background: transparent !important;

        &--variant-solo-filled {
          .v-field__overlay {
            background: transparent;
          }
        }
      }

      .v-field__field {
        textarea {
          padding: 8px 12px !important;
          font-size: 0.9rem;
          line-height: 1.4;
          caret-color: #1976d2;
        }
      }

      .v-field__append-inner {
        align-items: end;
        padding-bottom: 6px;
      }

      .v-input__control {
        min-height: 44px;
      }
    }
  }

  .message-input {
    :deep(textarea) {
      max-height: 200px;
      、 &::-webkit-scrollbar {
        display: none;
      }
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
  }

  .button-group {
    min-width: fit-content;
    padding-left: 4px;
  }

  .emoji-button,
  .record-button {
    transition: all 0.2s ease;

    &:hover {
      background-color: rgba(0, 0, 0, 0.04);
      transform: scale(1.05);
    }

    &:active {
      transform: scale(0.95);
    }
  }

  .send-button {
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    width: 40px;
    height: 40px;
    border-radius: 50%;

    &:hover:not(:disabled) {
      transform: scale(1.08);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }

    &:active:not(:disabled) {
      transform: scale(0.95);
    }
  }

  .input-footer {
    .recording-indicator {
      display: flex;
      align-items: center;
      animation: pulse 1.5s infinite;
      margin-top: 2px;
    }

    @keyframes pulse {
      0% {
        opacity: 1;
      }
      50% {
        opacity: 0.5;
      }
      100% {
        opacity: 1;
      }
    }
  }

  .emoji-picker {
    position: absolute;
    bottom: 100%;
    left: 0;
    right: 0;
    background: white;
    border-radius: 20px;
    margin-bottom: 16px;
    max-height: 250px;
    overflow: hidden;
    z-index: 100;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);

    .emoji-header {
      border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    }

    .emoji-grid {
      display: grid;
      grid-template-columns: repeat(8, 1fr);
      gap: 6px;
      max-height: 200px;
      overflow-y: auto;
      &::-webkit-scrollbar {
        display: none;
      }
      -ms-overflow-style: none;
      scrollbar-width: none;

      .emoji-item {
        text-align: center;
        font-size: 1.4rem;
        cursor: pointer;
        padding: 6px;
        border-radius: 10px;
        transition: all 0.2s ease;
        user-select: none;

        &:hover {
          background-color: #f0f8ff;
          transform: scale(1.2);
        }
      }
    }
  }

  @media (max-width: 959px) {
    padding: 14px !important;

    .emoji-picker {
      .emoji-grid {
        grid-template-columns: repeat(7, 1fr);
      }
    }
  }

  @media (max-width: 599px) {
    padding: 6px 8px !important;

    .input-container {
      padding: 2px 6px;
      border-radius: 20px;
    }

    :deep(.v-textarea) {
      .v-field__field {
        textarea {
          padding: 8px 10px !important;
          font-size: 0.95rem;
        }
      }
    }

    .emoji-button,
    .record-button {
      width: 34px;
      height: 34px;
    }

    .send-button {
      width: 38px;
      height: 38px;
    }

    .emoji-picker {
      .emoji-grid {
        grid-template-columns: repeat(6, 1fr);
        gap: 4px;
      }

      .emoji-item {
        font-size: 1.3rem;
        padding: 4px;
      }
    }
  }

  @media (max-width: 400px) {
    padding: 10px !important;

    .emoji-picker {
      .emoji-grid {
        grid-template-columns: repeat(5, 1fr);
      }
    }
  }
}
</style>
