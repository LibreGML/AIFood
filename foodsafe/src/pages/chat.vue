<template>
  <div class="chat-page">
    <AppBar />

    <div class="chat-container">
      <div class="chat-card elevation-2">
        <ChatHeader :show-clear-button="messages.length > 0" @clear-chat="clearChat" />

        <v-divider></v-divider>

        <MessageList
          :messages="messages"
          :user-initial="userInitial"
          :render-markdown="renderMarkdown"
          @send-quick-prompt="sendQuickPrompt"
          ref="messageListRef"
        />

        <v-divider></v-divider>

        <ChatInput
          :disabled="isLoading"
          @send-message="handleSendMessage"
          ref="chatInputRef"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import AppBar from "@/components/AppBar.vue";
import ChatHeader from "@/components/chat/ChatHeader.vue";
import ChatInput from "@/components/chat/ChatInput.vue";
import MessageList from "@/components/chat/MessageList.vue";
import { marked } from "marked";
import { computed, nextTick, onMounted, ref } from "vue";

const messages = ref([]);
const isLoading = ref(false);
const messageListRef = ref(null);
const chatInputRef = ref(null);

const isLoggedIn = computed(() => {
  return !!localStorage.getItem("token");
});

const loggedInUser = computed(() => {
  const userStr = localStorage.getItem("user");
  if (userStr) {
    try {
      return JSON.parse(userStr);
    } catch (e) {
      return { username: "用户" };
    }
  }
  return { username: "用户" };
});

const userInitial = computed(() => {
  const user = loggedInUser.value;
  return user.username ? user.username.charAt(0).toUpperCase() : "U";
});

const renderMarkdown = (text) => {
  if (!text) return "";
  return marked.parse(text, { breaks: true });
};

const handleSendMessage = async (message) => {
  if (!message.trim() || isLoading.value) return;

  const userMessage = {
    role: "user",
    content: message.trim(),
  };

  messages.value.push(userMessage);
  isLoading.value = true;

  try {
    scrollToBottom();
    await fetchAIResponse(message);
  } catch (error) {
    console.error("Error sending message:", error);
    const lastMessage = messages.value[messages.value.length - 1];
    if (lastMessage.role === "assistant") {
      lastMessage.content = "抱歉，我在处理您的请求时遇到了问题，请稍后再试。";
    } else {
      messages.value.push({
        role: "assistant",
        content: "抱歉，我在处理您的请求时遇到了问题，请稍后再试。",
      });
    }
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }
};

const fetchAIResponse = async (userInput) => {
  try {
    messages.value.push({
      role: "assistant",
      content: { type: "streaming", text: "" },
    });

    const aiMessageIndex = messages.value.length - 1;

    const history = messages.value.slice(0, -1).map((msg) => ({
      role: msg.role,
      content: typeof msg.content === "string" ? msg.content : msg.content.text,
    }));

    // 构建符合OpenAI格式的请求体
    const requestBody = {
      model: "gpt-3.5-turbo", // 适配本地模型
      messages: [...history, { role: "user", content: userInput }],
      stream: true, // 启用流式输出
    };

    // 使用本地部署的模型API
    const response = await fetch("http://localhost:8079/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`API error ${response.status}: ${JSON.stringify(errorData)}`);
    }

    // 处理流式响应
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let accumulatedText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split("\n").filter((line) => line.trim() !== "");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const dataStr = line.substring(6);

          if (dataStr === "[DONE]") {
            break;
          }

          try {
            const data = JSON.parse(dataStr);
            // 更灵活地处理可能的响应格式
            const content =
              data.choices?.[0]?.delta?.content ||
              data.choices?.[0]?.text ||
              data.content ||
              "";
            if (content) {
              accumulatedText += content;
              messages.value[aiMessageIndex].content = {
                type: "streaming",
                text: accumulatedText,
              };
              scrollToBottom();
            }
          } catch (e) {
            console.warn("Error parsing JSON:", e, "Raw line:", line);
          }
        }
      }
    }
  } catch (error) {
    console.error("API error details:", error);
    const lastMessage = messages.value[messages.value.length - 1];
    const errorMessage = `错误详情: ${error.message || error}\n请检查API配置是否正确`;

    if (lastMessage.role === "assistant") {
      lastMessage.content = errorMessage;
    } else {
      messages.value.push({
        role: "assistant",
        content: errorMessage,
      });
    }
  }
};

const sendQuickPrompt = (prompt) => {
  if (chatInputRef.value) {
    chatInputRef.value.inputMessage = prompt;
    nextTick(() => {
      handleSendMessage(prompt);
    });
  }
};

const clearChat = () => {
  messages.value = [];
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messageListRef.value && messageListRef.value.chatContainer) {
      messageListRef.value.chatContainer.scrollTop =
        messageListRef.value.chatContainer.scrollHeight;
    }
  });
};

onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped lang="scss">
.chat-page {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
  min-height: 100vh;
  padding: 0;
}

.chat-container {
  max-width: 100%;
  margin: 0 auto;
  height: 100vh;
  padding: 4px !important;

  @media (min-width: 600px) {
    padding: 8px !important;
    max-width: 1400px;
  }
}

.chat-card {
  height: calc(100vh - 8px);
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  @media (min-width: 600px) {
    height: calc(100vh - 16px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  }
}

@media (max-width: 599px) {
  .chat-card {
    height: calc(100vh - 16px);
  }
}
</style>
