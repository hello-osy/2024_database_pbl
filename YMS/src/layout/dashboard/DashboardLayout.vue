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
export default {
  data() {
    return {
      links: [
        { path: '/admin/dashboard', name: 'Dashboard', icon: 'ti-panel', 
          children: [
            { path: '/admin/yard1', name: 'Yard1'},
            { path: '/admin/yard2', name: 'Yard2'}
          ]
         },
        { path: '/admin/transportlog', name: 'Transport Log', icon: 'ti-receipt' },
        { path: '/admin/driverlist', name: 'Driver List', icon: 'ti-id-badge' },
        { path: '/admin/assignedmanagement', name: 'AssignedManagement', icon: 'ti-truck'}
      ],
    }
  },
  components: {
    TopNavbar,
    // ContentFooter,
    DashboardContent,
    MobileMenu,
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
  },
};
</script>
