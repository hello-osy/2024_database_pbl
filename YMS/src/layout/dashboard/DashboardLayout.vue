<template>
  <div class="wrapper">
    <side-bar :sidebarLinks="links">
      <!-- <template slot="links">
        <sidebar-link :to="{name: 'division'}" name="Division" icon="ti-map-alt" />
        <sidebar-link :to="{name: 'transportlog'}" name="Transport Log" icon="ti-receipt" />
        <sidebar-link :to="{name: 'driverprofiles'}" name="Driver Profiles" icon="ti-id-badge" />
        <sidebar-link :to="{name: 'dashboard'}" name="Dashboard" icon="ti-panel" />
        <sidebar-link :to="{name: 'yard1'}" name="Icons" icon="ti-pencil-alt2" />
      </template> -->
      <mobile-menu>
        <li class="nav-item">
          <a class="nav-link">
            <i class="ti-panel"></i>
            <p>Stats</p>
          </a>
        </li>
        <drop-down
          class="nav-item"
          title="5 Notifications"
          title-classes="nav-link"
          icon="ti-bell"
        >
          <a class="dropdown-item">Notification 1</a>
          <a class="dropdown-item">Notification 2</a>
          <a class="dropdown-item">Notification 3</a>
          <a class="dropdown-item">Notification 4</a>
          <a class="dropdown-item">Another notification</a>
        </drop-down>
        <li class="nav-item">
          <a class="nav-link">
            <i class="ti-settings"></i>
            <p>Settings</p>
          </a>
        </li>
        <li class="divider"></li>
      </mobile-menu>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar"> </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss"></style>
<script>
import TopNavbar from "./TopNavbar.vue";
// import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "./MobileMenu";
import AssignedManagement from "../../pages/Admin/AssignedManagement.vue";

import axios from "axios";


export default {
  data() {
    return {
      links: [
        {
          path: "/admin/dashboard",
          name: "Dashboard",
          icon: "ti-panel",
          children: [
            { path: "/admin/yard1", name: "HOU_YARD_0001" },
            // { path: "/admin/yard2", name: "HOU_YARD_0002" },
            // { path: "/admin/yard3", name: "LA_YARD_0001" },
            // { path: "/admin/yard4", name: "LA_YARD_0002" },
            // { path: "/admin/yard5", name: "MOB_YARD_0001" },
            // { path: "/admin/yard6", name: "MOB_YARD_0002" },
            // { path: "/admin/yard7", name: "PHX_YARD_0001" },
            // { path: "/admin/yard8", name: "PHX_YARD_0002" },
            // { path: "/admin/yard9", name: "SAV_YARD_0001" },
            // { path: "/admin/yard10", name: "SAV_YARD_0002" },
          ],
        },
        {
          path: "/admin/transportlog",
          name: "Transport Log",
          icon: "ti-receipt",
        },
        { path: "/admin/driverlist", name: "Driver List", icon: "ti-id-badge" },
        {
          path: "/admin/assignedmanagement",
          name: "AssignedManagement",
          icon: "ti-truck",
        },
      ],
    };
  },
  components: {
    TopNavbar,
    // ContentFooter,
    DashboardContent,
    MobileMenu,
  },
  methods: {
    async fetchYardLinks() {
      try {
        // Yard 데이터를 API에서 가져옴
        const response = await axios.get("/api/yard/all");

        if (response.data.success) {
          const yardLinks = response.data.data.map((yard) => ({
            path: `/admin/yard/${yard.id}`, // 동적 경로
            name: yard.name, // Yard 이름
            meta: { yardName: yard.name, yardId: yard.id }, // 추가 메타 데이터
          }));

          // "Dashboard" 링크의 children에 Yard 링크 추가
          const dashboardLink = this.links.find((link) => link.name === "Dashboard");
          if (dashboardLink) {
            dashboardLink.children = yardLinks;
          }
        }
        console.log("추가 성공적")
      } catch (error) {
        console.error("Error fetching yard links:", error.message);
      }
    },
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
  },
  mounted() {
    // 컴포넌트가 로드되면 Yard 링크를 가져와 추가
    this.fetchYardLinks();
  },
};
</script>
