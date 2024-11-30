<template>
  <div class="wrapper">
    <side-bar :sidebarLinks="links">
      <!-- <template slot="links">
        <sidebar-link to="/driver/profile" name="Profile" icon="ti-map-alt" />
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
import DashboardContent from "./Content.vue";
import MobileMenu from "./MobileMenu";
// import ContentFooter from "./ContentFooter.vue";
export default {
  data() {
    return {
      links: [
        { path: '/driver/driverdashboard', name: 'Dashboard', icon: 'ti-panel'},
        { path: '/driver/driverprofile', name: 'Profile', icon: 'ti-user'},
        { path: '/driver/driverschedule', name: 'Schedule', icon: 'ti-alarm-clock'},
        { path: '/driver/editprofile', name: 'EditProfile', icon: 'ti-pencil-alt'}
      ],
    }
  },
  components: {
    TopNavbar,
    DashboardContent,
    MobileMenu,
    // ContentFooter,
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
