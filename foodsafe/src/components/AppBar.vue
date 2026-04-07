<template>
  <v-app-bar app class="home-app-bar" scroll-behavior="hide" :elevation="5">
    <template v-slot:prepend>
      <v-app-bar-nav-icon
        @click="drawer = !drawer"
        icon="mdi-menu"
        color="success"
        class="d-md-none"
      ></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title
      @click="gotoHome"
      class="font-weight-bold text-subtitle-1 text-green-darken-4"
    >
      食品安全检测平台
    </v-app-bar-title>

    <template v-slot:append>
      <div class="d-none d-md-flex align-center">
        <v-btn
          v-for="(item, i) in navItems"
          :key="i"
          :prepend-icon="item.icon"
          variant="text"
          class="text-capitalize"
          @click="navigateTo(item.value)"
        >
          {{ item.title }}
        </v-btn>
      </div>
      <v-avatar
        size="36"
        color="success"
        class="mx-3"
        @click="goToProfile"
        style="cursor: pointer"
      >
        <span class="text-white font-weight-bold">{{
          isLoggedIn ? userInitial : "葛"
        }}</span>
      </v-avatar>
    </template>
  </v-app-bar>

  <v-navigation-drawer
    class="homeDrawer"
    v-model="drawer"
    temporary
    scrim="rgba(208, 255, 210, 0.8)"
  >
    <template v-slot:prepend>
      <div class="pa-3 d-flex align-center">
        <v-avatar
          size="48"
          color="success"
          class="mr-3"
          @click="goToProfile"
          style="cursor: pointer"
        >
          <span class="text-white font-weight-bold text-h5">{{
            isLoggedIn ? userInitial : "葛"
          }}</span>
        </v-avatar>
        <div>
          <div class="font-weight-bold">
            {{ isLoggedIn ? loggedInUser.username : "葛墨林" }}
          </div>
          <div class="text-caption">
            {{ isLoggedIn ? loggedInUser.email : "1778607946@qq.com" }}
          </div>
        </div>
      </div>
    </template>

    <v-divider></v-divider>

    <v-list nav>
      <v-list-item
        v-for="(item, i) in navItems"
        :key="i"
        :prepend-icon="item.icon"
        :title="item.title"
        :value="item.value"
        rounded="xl"
        class="pl-4"
        @click="navigateTo(item.value)"
      ></v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-4">
        <v-btn color="success" block rounded="xl" @click="loginOrLogout">
          {{ isLoggedIn ? "退出登录" : "登录" }}
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const navItems = [
  { title: "首页", value: "/", icon: "mdi-home" },
  { title: "AI检测", value: "/scan", icon: "mdi-camera-outline" },
  { title: "知识库", value: "/knowledge", icon: "mdi-book-open-outline" },
  { title: "查询历史", value: "/history", icon: "mdi-history" },
  { title: "AI助手", value: "/chat", icon: "mdi-robot-outline" },
];

// 检查是否已登录
const isLoggedIn = computed(() => {
  return !!localStorage.getItem("token");
});

// 获取登录用户信息
const loggedInUser = computed(() => {
  const userStr = localStorage.getItem("user");
  if (userStr) {
    try {
      return JSON.parse(userStr);
    } catch (e) {
      return { username: "用户", email: "user@example.com" };
    }
  }
  return { username: "葛墨林", email: "1778607946@qq.com" };
});

// 获取用户首字母
const userInitial = computed(() => {
  const user = loggedInUser.value;
  return user.username ? user.username.charAt(0).toUpperCase() : "U";
});

const drawer = ref(false);

const navigateTo = (route) => {
  router.push(route);
  drawer.value = false;
};

const gotoHome = () => {
  router.push("/");
};

const goToProfile = () => {
  if (isLoggedIn.value) {
    // 用户已登录，跳转到个人中心页面
    router.push("/profile");
  } else {
    // 用户未登录，跳转到登录页面
    router.push("/login");
  }
};

const loginOrLogout = () => {
  if (isLoggedIn.value) {
    // 退出登录
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    // 退出登录后返回首页
    router.push("/");
  } else {
    // 前往登录页面
    router.push("/login");
  }
  drawer.value = false;
};
</script>

<style scoped lang="scss">
.home-app-bar,
.homeDrawer {
  background-color: rgba(252, 253, 255, 0.7) !important;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);

  @media (max-width: 960px) {
    padding-inline: 8px;
  }
}

@media (max-width: 600px) {
  .home-app-bar :deep(.v-toolbar-title) {
    font-size: 1rem !important;
  }

  .home-app-bar {
    height: 56px !important;
  }
}
</style>
