<template>
  <div class="wrapper">
    <!-- 새로운 SideBarDriver 컴포넌트를 추가 -->
    <side-bar-driver />
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content> </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue";
import DashboardContent from "./Content.vue";
import ContentFooter from "./ContentFooter.vue";
import SideBarDriver from "./SideBar_driver.vue"; // 새로운 사이드바 컴포넌트 추가

export default {
  components: {
    TopNavbar,
    DashboardContent,
    ContentFooter,
    SideBarDriver,
  },
};
</script>

<style scoped>
.wrapper {
  display: flex;
  height: 100vh;
}

.main-panel {
  flex: 1;
  overflow-y: auto; /* 스크롤 가능 */
}

.sidebar-driver {
  flex-shrink: 0;
}
</style>
