<template>
  <div class="profile-page">
    <AppBar />
    <v-container class="py-6">
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <!-- 用户信息头部 -->
          <v-card class="profile-card mb-6" elevation="0">
            <div class="profile-header">
              <div class="avatar-container">
                <v-avatar size="100" class="user-avatar">
                  <span class="text-h3 font-weight-bold text-white">{{
                    userInitial
                  }}</span>
                </v-avatar>
              </div>
              <div class="user-info">
                <h2 class="text-h3 font-weight-bold text-white">{{ user.username }}</h2>
                <p class="text-subtitle-1 text-white mb-0">{{ user.email }}</p>
                <p class="text-caption text-white mt-2">
                  注册于 {{ formatRegistrationDate(user.createdAt) }}
                </p>
              </div>
            </div>
          </v-card>

          <!-- 主要内容区域 -->
          <v-row>
            <!-- 个人资料部分 -->
            <v-col cols="12" md="8">
              <v-card class="info-card" elevation="0">
                <v-card-title class="card-title">
                  <v-icon size="large" color="success" class="mr-2"
                    >mdi-account-details</v-icon
                  >
                  <span>个人资料</span>
                </v-card-title>

                <v-card-text class="pa-6">
                  <div class="info-item">
                    <v-icon color="success" class="mr-3">mdi-account-outline</v-icon>
                    <div class="info-content">
                      <div class="info-label">用户名</div>
                      <div class="info-value">{{ user.username }}</div>
                    </div>
                  </div>

                  <div class="info-item mt-4">
                    <v-icon color="success" class="mr-3">mdi-email-outline</v-icon>
                    <div class="info-content">
                      <div class="info-label">邮箱地址</div>
                      <div class="info-value">{{ user.email }}</div>
                    </div>
                  </div>

                  <div class="info-item mt-4">
                    <v-icon color="success" class="mr-3">mdi-calendar</v-icon>
                    <div class="info-content">
                      <div class="info-label">注册时间</div>
                      <div class="info-value">
                        {{ formatRegistrationDate(user.createdAt) }}
                      </div>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- 操作选项 -->
            <v-col cols="12" md="4">
              <v-card class="actions-card" elevation="0">
                <v-card-title class="card-title">
                  <v-icon size="large" color="success" class="mr-2">mdi-cog</v-icon>
                  <span>账户操作</span>
                </v-card-title>

                <v-card-text class="pa-6">
                  <v-btn
                    class="action-btn mb-4"
                    block
                    size="large"
                    color="success"
                    rounded="xl"
                    @click="changePassword"
                  >
                    <v-icon start>mdi-lock-reset</v-icon>
                    修改密码
                  </v-btn>

                  <v-btn
                    class="action-btn"
                    block
                    size="large"
                    color="success"
                    variant="outlined"
                    rounded="xl"
                    @click="logout"
                  >
                    <v-icon start>mdi-logout</v-icon>
                    退出登录
                  </v-btn>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>

    <!-- 修改密码对话框 -->
    <v-dialog v-model="changePasswordDialog" max-width="500">
      <v-card>
        <v-card-title class="card-title">
          <v-icon size="large" color="success" class="mr-2">mdi-lock-reset</v-icon>
          <span>修改密码</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="passwordForm" v-model="passwordFormValid">
            <v-text-field
              v-model="passwordForm.oldPassword"
              :rules="oldPasswordRules"
              label="旧密码"
              prepend-inner-icon="mdi-lock-outline"
              :type="showOldPassword ? 'text' : 'password'"
              :append-inner-icon="showOldPassword ? 'mdi-eye' : 'mdi-eye-off'"
              variant="outlined"
              required
              class="mb-4"
              @click:append-inner="showOldPassword = !showOldPassword"
            ></v-text-field>

            <v-text-field
              v-model="passwordForm.newPassword"
              :rules="newPasswordRules"
              label="新密码"
              prepend-inner-icon="mdi-lock-outline"
              :type="showNewPassword ? 'text' : 'password'"
              :append-inner-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
              variant="outlined"
              required
              class="mb-4"
              @click:append-inner="showNewPassword = !showNewPassword"
            ></v-text-field>

            <v-text-field
              v-model="passwordForm.confirmPassword"
              :rules="confirmPasswordRules"
              label="确认新密码"
              prepend-inner-icon="mdi-lock-outline"
              :type="showConfirmPassword ? 'text' : 'password'"
              :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
              variant="outlined"
              required
              class="mb-4"
              @click:append-inner="showConfirmPassword = !showConfirmPassword"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="closePasswordDialog">取消</v-btn>
          <v-btn
            color="success"
            :loading="passwordFormLoading"
            @click="submitPasswordChange"
          >
            确认修改
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000" top>
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar.show = false"> 关闭 </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import AppBar from "@/components/AppBar.vue";
import { inject, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const $http = inject("$http");

const user = ref({
  username: "",
  email: "",
  createdAt: "", // 使用 createdAt 字段匹配后端
});

const userInitial = ref("");

const changePasswordDialog = ref(false);
const passwordForm = ref({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
});
const passwordFormValid = ref(false);
const passwordFormLoading = ref(false);
const showOldPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

const snackbar = ref({
  show: false,
  text: "",
  color: "",
});

const oldPasswordRules = [
  (v) => !!v || "请输入旧密码",
  (v) => (v && v.length >= 6) || "密码至少6个字符",
];

const newPasswordRules = [
  (v) => !!v || "请输入新密码",
  (v) => (v && v.length >= 6) || "密码至少6个字符",
  (v) => (v && v.length <= 20) || "密码不得超过20个字符",
];

const confirmPasswordRules = [
  (v) => !!v || "请确认新密码",
  (v) => v === passwordForm.value.newPassword || "两次输入的密码不一致",
];

const formatRegistrationDate = (dateString) => {
  if (!dateString) return "未知";
  const date = new Date(dateString);
  return date.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const fetchUserInfo = async () => {
  try {
    const response = await $http.get("/auth/user-info");
    const { data } = response.data;
    user.value = { ...user.value, ...data };
    userInitial.value = data.username ? data.username.charAt(0).toUpperCase() : "U";
  } catch (error) {
    console.error("获取用户信息失败", error);
    snackbar.value = {
      show: true,
      text: "获取用户信息失败",
      color: "error",
    };
  }
};

const changePassword = () => {
  changePasswordDialog.value = true;
  passwordForm.value = {
    oldPassword: "",
    newPassword: "",
    confirmPassword: "",
  };
};

const closePasswordDialog = () => {
  changePasswordDialog.value = false;
};

const submitPasswordChange = async () => {
  const { valid } = await passwordForm.value.validate();
  if (!valid) return;

  passwordFormLoading.value = true;

  try {
    await $http.post("/auth/change-password", {
      oldPassword: passwordForm.value.oldPassword,
      newPassword: passwordForm.value.newPassword,
    });

    snackbar.value = {
      show: true,
      text: "密码修改成功",
      color: "success",
    };

    closePasswordDialog();
  } catch (error) {
    const errorMsg = error.response?.data?.message || "密码修改失败";
    snackbar.value = {
      show: true,
      text: errorMsg,
      color: "error",
    };
  } finally {
    passwordFormLoading.value = false;
  }
};

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  router.push("/login");
};

onMounted(() => {
  fetchUserInfo();
});
</script>

<style scoped lang="scss">
.profile-page {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  min-height: 100vh;
  padding-bottom: 40px;
}

.profile-card {
  background: linear-gradient(135deg, #4caf50 0%, #81c784 100%);
  border-radius: 24px;
  overflow: visible;
  position: relative;
  box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  text-align: center;

  @media (min-width: 768px) {
    flex-direction: row;
    text-align: left;
    padding: 50px;
  }
}

.avatar-container {
  margin-bottom: 20px;
  @media (min-width: 768px) {
    margin-bottom: 0;
    margin-right: 30px;
  }
}

.user-avatar {
  border: 4px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.user-info {
  flex: 1;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  padding: 20px 24px 10px;
  display: flex;
  align-items: center;
}

.info-card,
.actions-card {
  border-radius: 24px;
  overflow: hidden;
  background: white;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  }
}

.info-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 16px;
  background: #f1f8e9;
  transition: all 0.3s ease;

  &:hover {
    background: #e8f5e9;
    transform: translateX(5px);
  }
}

.info-content {
  flex: 1;
}

.info-label {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 4px;
}

.info-value {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
}

.action-btn {
  text-transform: none;
  font-weight: 500;
  letter-spacing: 0.5px;
  padding: 20px;
  font-size: 1rem;
  border-radius: 16px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1) !important;
  }

  &:active {
    transform: translateY(0);
  }
}
</style>
