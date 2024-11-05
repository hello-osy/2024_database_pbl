<!-- src/App.vue -->
<template>
  <div class="app-wrapper">
    <!-- Sidebar 유지 -->
    <sidebar />

    <!-- 메인 콘텐츠 -->
    <div class="main-content">
      <notifications></notifications>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/SidebarPlugin/SideBar.vue";

export default {
  components: {
    Sidebar,
  },
};
</script>

<style scoped>
.app-wrapper {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-left: 250px; /* Sidebar 너비와 일치시킴 */
  overflow-y: auto; /* 스크롤링 가능 */
}
</style>
