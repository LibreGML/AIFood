<template>
  <div class="auth-container">
    <v-card class="auth-card" elevation="24">
      <div class="auth-header">
        <v-icon size="x-large" color="primary">{{
          isLogin ? "mdi-login" : "mdi-account-plus"
        }}</v-icon>
        <h2 class="text-h4 font-weight-bold mt-2">
          {{ isLogin ? "欢迎回来" : "创建账户" }}
        </h2>
        <p class="text-medium-emphasis">
          {{ isLogin ? "登录您的账户" : "填写信息创建新账户" }}
        </p>
      </div>

      <v-card-text class="auth-content">
        <v-alert
          v-if="errorMessage"
          type="error"
          variant="tonal"
          class="mb-4"
          density="comfortable"
          closable
          @click:close="errorMessage = ''"
        >
          {{ errorMessage }}
        </v-alert>

        <v-alert
          v-if="successMessage"
          type="success"
          variant="tonal"
          class="mb-4"
          density="comfortable"
          closable
          @click:close="successMessage = ''"
        >
          {{ successMessage }}
        </v-alert>

        <v-form ref="form" v-model="valid" @submit.prevent="handleSubmit">
          <v-text-field
            v-model="authForm.username"
            :rules="usernameRules"
            :label="isLogin ? '用户名' : '用户名'"
            prepend-inner-icon="mdi-account-outline"
            variant="outlined"
            clearable
            required
            class="mb-4"
            density="comfortable"
            :loading="loading"
          ></v-text-field>

          <v-text-field
            v-model="authForm.email"
            :rules="emailRules"
            label="邮箱地址"
            prepend-inner-icon="mdi-email-outline"
            variant="outlined"
            type="email"
            clearable
            required
            class="mb-4"
            density="comfortable"
            :loading="loading"
          ></v-text-field>

          <v-text-field
            v-model="authForm.password"
            :rules="passwordRules"
            label="密码"
            prepend-inner-icon="mdi-lock-outline"
            :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showPassword ? 'text' : 'password'"
            variant="outlined"
            required
            class="mb-4"
            density="comfortable"
            :loading="loading"
            @click:append-inner="showPassword = !showPassword"
          ></v-text-field>

          <template v-if="!isLogin">
            <v-text-field
              v-model="authForm.confirmPassword"
              :rules="confirmPasswordRules"
              label="确认密码"
              prepend-inner-icon="mdi-lock-check-outline"
              :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showConfirmPassword ? 'text' : 'password'"
              variant="outlined"
              required
              class="mb-4"
              density="comfortable"
              :loading="loading && !isLogin"
              @click:append-inner="showConfirmPassword = !showConfirmPassword"
            ></v-text-field>
          </template>

          <div class="d-flex align-center mb-4" v-if="isLogin">
            <v-checkbox
              v-model="rememberMe"
              label="记住我"
              hide-details
              density="compact"
              color="primary"
            ></v-checkbox>

            <v-spacer></v-spacer>

            <v-btn variant="text" color="primary" size="small" @click="forgotPassword">
              忘记密码?
            </v-btn>
          </div>

          <v-btn
            :disabled="!valid || loading"
            :loading="loading"
            block
            :color="isLogin ? 'primary' : 'success'"
            size="large"
            type="submit"
            class="mt-2"
          >
            {{ isLogin ? "登录" : "注册" }}
          </v-btn>
        </v-form>
      </v-card-text>

      <v-card-actions class="auth-footer">
        <p class="text-body-2 text-medium-emphasis">
          {{ isLogin ? "还没有账户?" : "已有账户?" }}
          <v-btn variant="plain" color="primary" @click="toggleAuthMode" class="px-1">
            {{ isLogin ? "立即注册" : "立即登录" }}
          </v-btn>
        </p>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
import axios from "axios";
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const form = ref();
const valid = ref(false);
const loading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const rememberMe = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const isLogin = ref(true);

// 表单数据
const authForm = reactive({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
});

// 验证规则
const usernameRules = [
  (v) => !!v || "请输入用户名",
  (v) => (v && v.length >= 3) || "用户名至少3个字符",
  (v) => (v && v.length <= 20) || "用户名不得超过20个字符",
];

const emailRules = [
  (v) => !!v || "请输入邮箱地址",
  (v) => /.+@.+\..+/.test(v) || "请输入有效的邮箱地址",
];

const passwordRules = [
  (v) => !!v || "请输入密码",
  (v) => (v && v.length >= 6) || "密码至少6个字符",
  (v) => (v && v.length <= 20) || "密码不得超过20个字符",
];

const confirmPasswordRules = [
  (v) => !!v || "请确认密码",
  (v) => v === authForm.password || "两次输入的密码不一致",
];

// 切换登录/注册模式
const toggleAuthMode = () => {
  isLogin.value = !isLogin.value;
  errorMessage.value = "";
  successMessage.value = "";
  // 清空表单
  authForm.username = "";
  authForm.email = "";
  authForm.password = "";
  authForm.confirmPassword = "";
  // 重置表单验证
  if (form.value) {
    form.value.resetValidation();
  }
};

// 忘记密码处理
const forgotPassword = () => {
  errorMessage.value = "请联系管理员重置密码";
};

// 处理提交
const handleSubmit = async () => {
  const { valid } = await form.value.validate();

  if (valid) {
    loading.value = true;
    errorMessage.value = "";
    successMessage.value = "";

    try {
      if (isLogin.value) {
        await loginUser();
      } else {
        await registerUser();
      }
    } catch (error) {
      handleError(error);
    } finally {
      loading.value = false;
    }
  }
};

// 登录用户
const loginUser = async () => {
  try {
    const response = await axios.post("http://localhost:8080/api/auth/login", {
      username: authForm.username,
      email: authForm.email,
      password: authForm.password,
    });

    const { data } = response.data;
    const { token, user } = data;
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));

    successMessage.value = "登录成功！正在跳转...";

    setTimeout(() => {
      router.push("/");
    }, 1500);
  } catch (error) {
    throw error;
  }
};

const registerUser = async () => {
  try {
    const response = await axios.post("http://localhost:8080/api/auth/register", {
      username: authForm.username,
      email: authForm.email,
      password: authForm.password,
    });

    successMessage.value = response.data.message || "注册成功！请登录您的账户";
  } catch (error) {
    throw error;
  }
};

// 错误处理
const handleError = (error) => {
  if (error.response) {
    const { status, data } = error.response;

    if (data && data.message) {
      errorMessage.value = data.message;
      return;
    }

    switch (status) {
      case 400:
        errorMessage.value = "请求参数错误，请检查输入";
        break;
      case 401:
        errorMessage.value = "用户名或密码错误";
        break;
      case 409:
        errorMessage.value = "该邮箱已被注册";
        break;
      case 500:
        errorMessage.value = "服务器内部错误，请稍后再试";
        break;
      default:
        errorMessage.value = `操作失败: ${data.message || "未知错误"}`;
    }
  } else if (error.request) {
    errorMessage.value = "网络连接失败，请检查网络设置";
  } else {
    errorMessage.value = `请求失败: ${error.message}`;
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #63acff 0%, #abcfff 100%);
}

.auth-card {
  width: 100%;
  max-width: 480px;
  border-radius: 24px;
  overflow: hidden;
}

.auth-header {
  padding: 32px 32px 24px;
  text-align: center;
  background-color: white;
}

.auth-content {
  padding: 24px 32px 16px;
  background-color: white;
}

.auth-footer {
  padding: 16px 32px 24px;
  justify-content: center;
  background-color: white;
}

.v-btn {
  text-transform: none;
  letter-spacing: normal;
}
</style>
